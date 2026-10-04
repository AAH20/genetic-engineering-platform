"""Flux Balance Analysis (FBA) implementation for metabolic modeling."""
from collections import deque


class Reaction:
    """A metabolic reaction with stoichiometry and bounds."""

    def __init__(self, name, stoichiometry, lower_bound=0.0, upper_bound=1000.0):
        self.name = name
        self.stoichiometry = stoichiometry
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound


class MetabolicModel:
    """A metabolic model with reactions, metabolites, and flux bounds."""

    def __init__(self):
        self.reactions = {}
        self.metabolites = set()
        self.objective = None
        self._solution = None

    def add_reaction(self, name, stoich, lower_bound=0.0, upper_bound=1000.0):
        """Add a reaction with stoichiometry."""
        if name in self.reactions:
            raise ValueError(f"Reaction '{name}' already exists")
        self.reactions[name] = Reaction(name, stoich, lower_bound, upper_bound)
        for met in stoich:
            self.metabolites.add(met)

    def set_objective(self, reaction_name):
        """Set the objective reaction to maximize."""
        if reaction_name not in self.reactions:
            raise ValueError(f"Reaction '{reaction_name}' not found")
        self.objective = reaction_name

    def solve_fba(self):
        """Solve FBA using a greedy LP approximation.

        Returns dict mapping reaction name -> flux.
        """
        if not self.reactions:
            return {}

        if self.objective is None:
            raise ValueError("No objective set")

        fluxes = {}
        obj_rxn = self.reactions[self.objective]

        # Find max flux through objective
        max_flux = obj_rxn.upper_bound

        # Check substrate availability
        for met, coeff in obj_rxn.stoichiometry.items():
            if coeff < 0:  # substrate
                supply = 0
                for rxn_name, rxn in self.reactions.items():
                    if rxn_name == self.objective:
                        continue
                    s = rxn.stoichiometry.get(met, 0)
                    if s > 0:
                        supply += rxn.upper_bound * s
                if supply > 0:
                    max_flux = min(max_flux, supply / abs(coeff))

        fluxes[self.objective] = max_flux

        # Propagate fluxes through connected reactions
        for rxn_name, rxn in self.reactions.items():
            if rxn_name == self.objective:
                continue
            shared = set(rxn.stoichiometry.keys()) & set(obj_rxn.stoichiometry.keys())
            if shared:
                fluxes[rxn_name] = max_flux
            else:
                fluxes[rxn_name] = 0.0

        self._solution = fluxes
        return fluxes

    def calculate_flux(self, reaction_name):
        """Get the flux for a reaction, auto-solving if needed."""
        if reaction_name not in self.reactions:
            raise ValueError(f"Reaction '{reaction_name}' not found")
        if self._solution is None:
            self.solve_fba()
        return self._solution.get(reaction_name, 0.0)


class PathwayDesigner:
    """Design metabolic pathways from substrate to product."""

    def __init__(self, model):
        self.model = model

    def design_pathway(self, substrate, product):
        """Find a path of reactions from substrate to product using BFS."""
        if substrate == product:
            return []

        # Build metabolite -> reactions graph
        met_to_rxn = {}
        for rxn_name, rxn in self.model.reactions.items():
            for met in rxn.stoichiometry:
                if met not in met_to_rxn:
                    met_to_rxn[met] = []
                met_to_rxn[met].append(rxn_name)

        if substrate not in met_to_rxn or product not in met_to_rxn:
            return []

        # BFS from substrate to product
        queue = deque([(substrate, [])])
        visited_mets = {substrate}
        visited_rxns = set()

        while queue:
            current_met, path = queue.popleft()

            for rxn_name in met_to_rxn.get(current_met, []):
                if rxn_name in visited_rxns:
                    continue
                visited_rxns.add(rxn_name)
                rxn = self.model.reactions[rxn_name]
                new_path = path + [rxn_name]

                for met, coeff in rxn.stoichiometry.items():
                    if coeff > 0 and met == product:
                        return new_path
                    if coeff > 0 and met not in visited_mets:
                        visited_mets.add(met)
                        queue.append((met, new_path))

        return []

    def calculate_pathway_yield(self, pathway):
        """Calculate theoretical yield of product from substrate."""
        if not pathway:
            return 0.0

        total_substrate = 0
        total_product = 0

        for rxn_name in pathway:
            rxn = self.model.reactions[rxn_name]
            for met, coeff in rxn.stoichiometry.items():
                if coeff < 0:
                    total_substrate = max(total_substrate, abs(coeff))
                if coeff > 0:
                    total_product = max(total_product, coeff)

        if total_substrate == 0:
            return 0.0

        return total_product / total_substrate


class StrainOptimizer:
    """Optimize strain by identifying beneficial knockouts."""

    def __init__(self, model):
        self.model = model

    def optimize_knockouts(self):
        """Identify beneficial knockouts to improve target product yield."""
        if not self.model.reactions or self.model.objective is None:
            return []

        knockouts = []
        obj_stoich = self.model.reactions[self.model.objective].stoichiometry

        # Find reactions that compete for substrates in the objective pathway
        for rxn_name, rxn in self.model.reactions.items():
            if rxn_name == self.model.objective:
                continue
            for met, coeff in rxn.stoichiometry.items():
                if coeff < 0 and met in obj_stoich:
                    knockouts.append(rxn_name)
                    break

        return knockouts
