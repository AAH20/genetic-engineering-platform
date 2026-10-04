"""Flux Balance Analysis (FBA) implementation for metabolic modeling."""
from collections import deque

import numpy as np
from scipy.optimize import linprog


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

    def fva(self, fraction_of_optimum=0.95):
        """Flux Variability Analysis.

        Compute min/max flux for each reaction while maintaining
        >= fraction_of_optimum * optimal objective value.

        Returns dict mapping reaction name -> {'min': float, 'max': float}.
        """
        if not self.reactions:
            return {}

        if self.objective is None:
            raise ValueError("No objective set")

        rxn_names = list(self.reactions.keys())
        n_rxns = len(rxn_names)

        # Identify internal metabolites (appear in 2+ reactions)
        met_count = {}
        for rxn in self.reactions.values():
            for met in rxn.stoichiometry:
                met_count[met] = met_count.get(met, 0) + 1

        internal_mets = [m for m in self.metabolites if met_count[m] >= 2]

        # Build stoichiometry matrix for internal metabolites
        if internal_mets:
            s_matrix = np.zeros((len(internal_mets), n_rxns))
            met_idx = {m: i for i, m in enumerate(internal_mets)}
            for j, rxn_name in enumerate(rxn_names):
                rxn = self.reactions[rxn_name]
                for met, coeff in rxn.stoichiometry.items():
                    if met in met_idx:
                        s_matrix[met_idx[met], j] = coeff
            b_eq = np.zeros(len(internal_mets))
        else:
            s_matrix = None
            b_eq = None

        # Bounds
        bounds = [(self.reactions[r].lower_bound, self.reactions[r].upper_bound) for r in rxn_names]

        # Solve FBA to get optimal objective value
        c = np.zeros(n_rxns)
        obj_idx = rxn_names.index(self.objective)
        c[obj_idx] = -1.0

        result = linprog(c, A_eq=s_matrix, b_eq=b_eq, bounds=bounds, method='highs')

        if not result.success:
            raise ValueError(f"FBA solve failed: {result.message}")

        optimal_obj = -result.fun

        # Constraint: objective >= fraction_of_optimum * optimal_obj
        a_ub = np.zeros((1, n_rxns))
        a_ub[0, obj_idx] = -1.0
        b_ub = np.array([-fraction_of_optimum * optimal_obj])

        # For each reaction, minimize and maximize its flux
        fva_result = {}
        for i, rxn_name in enumerate(rxn_names):
            # Minimize v_i
            c_min = np.zeros(n_rxns)
            c_min[i] = 1.0
            res_min = linprog(
                c_min, A_ub=a_ub, b_ub=b_ub, A_eq=s_matrix,
                b_eq=b_eq, bounds=bounds, method='highs',
            )

            # Maximize v_i
            c_max = np.zeros(n_rxns)
            c_max[i] = -1.0
            res_max = linprog(
                c_max, A_ub=a_ub, b_ub=b_ub, A_eq=s_matrix,
                b_eq=b_eq, bounds=bounds, method='highs',
            )

            if not res_min.success or not res_max.success:
                raise ValueError(f"FVA solve failed for {rxn_name}")

            fva_result[rxn_name] = {
                'min': float(res_min.fun),
                'max': float(-res_max.fun),
            }

        return fva_result


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

    def simulate_knockout(self, reaction_name):
        """Simulate knockout of a reaction and return flux change information.

        Saves current bounds, sets reaction bounds to (0, 0), re-solves FBA,
        restores original bounds, and returns a dict with results.
        """
        if reaction_name not in self.model.reactions:
            raise ValueError(f"Reaction '{reaction_name}' not found")

        rxn = self.model.reactions[reaction_name]
        original_lower = rxn.lower_bound
        original_upper = rxn.upper_bound

        # Get original flux
        original_flux = self.model.calculate_flux(self.model.objective)

        # Knock out the reaction
        rxn.lower_bound = 0.0
        rxn.upper_bound = 0.0
        self.model._solution = None  # Force re-solve

        # Re-solve and get knockout flux
        knockout_flux = self.model.calculate_flux(self.model.objective)

        # Restore original bounds
        rxn.lower_bound = original_lower
        rxn.upper_bound = original_upper
        self.model._solution = None  # Force re-solve back

        return {
            "reaction": reaction_name,
            "original_flux": original_flux,
            "knockout_flux": knockout_flux,
            "objective_change": knockout_flux - original_flux,
        }

    def compare_knockouts(self, reaction_names):
        """Compare multiple knockouts and return results sorted by objective_change."""
        if not reaction_names:
            return []

        results = []
        for name in reaction_names:
            results.append(self.simulate_knockout(name))

        results.sort(key=lambda r: r["objective_change"])
        return results
