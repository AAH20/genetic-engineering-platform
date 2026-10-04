"""Flux Balance Analysis (FBA) implementation for metabolic modeling."""
from collections import deque

import numpy as np
from scipy.optimize import linprog


class Reaction:
    """A metabolic reaction with stoichiometry, bounds, and GPR rules."""

    def __init__(self, name, stoichiometry, lower_bound=0.0, upper_bound=1000.0):
        self.name = name
        self.stoichiometry = stoichiometry
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.gpr_rule: str | None = None


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

    def add_gpr_rule(self, reaction_name: str, rule: str) -> None:
        """Add a Gene-Protein-Reaction rule to a reaction.

        Args:
            reaction_name: Name of the reaction.
            rule: GPR rule string (e.g., 'gene1 and gene2', 'gene1 or gene2').

        Raises:
            ValueError: If reaction_name is not found.
        """
        if reaction_name not in self.reactions:
            raise ValueError(f"Reaction '{reaction_name}' not found")
        self.reactions[reaction_name].gpr_rule = rule

    def get_reactions_by_gene(self, gene: str) -> list[str]:
        """Get all reaction names associated with a gene via GPR rules.

        Args:
            gene: Gene identifier.

        Returns:
            List of reaction names whose GPR rules mention the gene.
        """
        result = []
        for rxn_name, rxn in self.reactions.items():
            if rxn.gpr_rule and gene in rxn.gpr_rule:
                result.append(rxn_name)
        return result

    def knockout_gene(self, gene: str) -> None:
        """Knock out a gene by disabling all reactions whose GPR rules mention it.

        Args:
            gene: Gene identifier.

        Raises:
            ValueError: If gene is not found in any GPR rule.
        """
        reactions = self.get_reactions_by_gene(gene)
        if not reactions:
            raise ValueError(f"Gene '{gene}' not found in any GPR rule")
        for rxn_name in reactions:
            self.reactions[rxn_name].lower_bound = 0.0
            self.reactions[rxn_name].upper_bound = 0.0
        self._solution = None

    def add_exchange_reaction(
        self, name: str, metabolite: str,
        lower_bound: float = -10.0, upper_bound: float = 1000.0,
    ) -> None:
        """Add an exchange reaction for nutrient uptake or product secretion.

        Args:
            name: Reaction name (e.g., 'EX_A').
            metabolite: Metabolite identifier.
            lower_bound: Lower bound (negative for uptake, 0 for secretion).
            upper_bound: Upper bound.

        Raises:
            ValueError: If metabolite is not in the model.
        """
        self.metabolites.add(metabolite)
        self.add_reaction(name, {metabolite: 1}, lower_bound, upper_bound)

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

    def robustness_analysis(self, reaction_name: str, fold_change: float = 0.5) -> dict:
        """Analyze robustness of objective to changes in reaction bounds.

        Args:
            reaction_name: Name of the reaction to perturb.
            fold_change: Factor to multiply the reaction bounds by.

        Returns:
            Dict with original_flux, perturbed_flux, fold_change, is_robust.
        """
        if reaction_name not in self.reactions:
            raise ValueError(f"Reaction '{reaction_name}' not found")
        if self.objective is None:
            raise ValueError("No objective set")

        rxn = self.reactions[reaction_name]
        original_lower = rxn.lower_bound
        original_upper = rxn.upper_bound

        # Get original flux
        original_flux = self.calculate_flux(self.objective)

        # Perturb bounds
        rxn.lower_bound = original_lower * fold_change
        rxn.upper_bound = original_upper * fold_change
        self._solution = None

        # Re-solve
        perturbed_flux = self.calculate_flux(self.objective)

        # Restore bounds
        rxn.lower_bound = original_lower
        rxn.upper_bound = original_upper
        self._solution = None

        # Determine robustness: robust if perturbed flux is at least 50% of original
        is_robust = perturbed_flux >= original_flux * 0.5

        return {
            "original_flux": original_flux,
            "perturbed_flux": perturbed_flux,
            "fold_change": fold_change,
            "is_robust": is_robust,
        }

    def shadow_prices(self) -> dict[str, float]:
        """Calculate shadow prices for all metabolites.

        Shadow price = change in objective value per unit change in metabolite availability.

        Returns:
            Dict mapping metabolite name to shadow price.
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

        # Solve FBA
        c = np.zeros(n_rxns)
        obj_idx = rxn_names.index(self.objective)
        c[obj_idx] = -1.0

        result = linprog(c, A_eq=s_matrix, b_eq=b_eq, bounds=bounds, method='highs')

        if not result.success:
            raise ValueError(f"FBA solve failed: {result.message}")

        # Shadow prices are the dual variables (marginals) of the equality constraints
        shadow_prices = {}
        if internal_mets and result.eqlin is not None:
            marginals = result.eqlin.marginals
            for i, met in enumerate(internal_mets):
                shadow_prices[met] = float(marginals[i])

        return shadow_prices

    def sample_flux_space(self, n_samples: int = 100, seed: int = 42) -> list[dict]:
        """Sample points from the flux space using the hit-and-run algorithm.

        Args:
            n_samples: Number of flux samples to generate.
            seed: Random seed for reproducibility.

        Returns:
            List of dicts mapping reaction name -> flux value.

        Raises:
            ValueError: If no objective is set or no feasible point exists.
        """
        if not self.reactions:
            return []
        if self.objective is None:
            raise ValueError("No objective set")

        rng = np.random.default_rng(seed)
        rxn_names = list(self.reactions.keys())
        n_rxns = len(rxn_names)

        # Build S matrix for internal metabolites
        met_count = {}
        for rxn in self.reactions.values():
            for met in rxn.stoichiometry:
                met_count[met] = met_count.get(met, 0) + 1
        internal_mets = [m for m in self.metabolites if met_count[m] >= 2]

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

        bounds = [
            (self.reactions[r].lower_bound, self.reactions[r].upper_bound)
            for r in rxn_names
        ]

        # Find a feasible starting point
        c = np.zeros(n_rxns)
        result = linprog(
            c, A_eq=s_matrix, b_eq=b_eq, bounds=bounds, method="highs"
        )
        if not result.success:
            raise ValueError("Could not find feasible starting point")

        current = result.x.copy()

        # Compute null space of S for direction generation
        if s_matrix is not None and s_matrix.shape[0] > 0:
            _, _, vh = np.linalg.svd(s_matrix)
            rank = np.linalg.matrix_rank(s_matrix)
            null_space = vh[rank:].T
        else:
            null_space = np.eye(n_rxns)

        samples = []
        for _ in range(n_samples):
            # Generate random direction in null space
            if null_space.shape[1] > 0:
                coeffs = rng.standard_normal(null_space.shape[1])
                direction = null_space @ coeffs
            else:
                direction = np.zeros(n_rxns)

            norm = np.linalg.norm(direction)
            if norm < 1e-12:
                samples.append(
                    {name: float(current[i]) for i, name in enumerate(rxn_names)}
                )
                continue
            direction = direction / norm

            # Find feasible step range
            t_min = -np.inf
            t_max = np.inf
            for i in range(n_rxns):
                if direction[i] > 1e-12:
                    t_max = min(t_max, (bounds[i][1] - current[i]) / direction[i])
                    t_min = max(t_min, (bounds[i][0] - current[i]) / direction[i])
                elif direction[i] < -1e-12:
                    t_max = min(t_max, (bounds[i][0] - current[i]) / direction[i])
                    t_min = max(t_min, (bounds[i][1] - current[i]) / direction[i])

            if t_min >= t_max:
                samples.append(
                    {name: float(current[i]) for i, name in enumerate(rxn_names)}
                )
                continue

            t = rng.uniform(t_min, t_max)
            current = current + t * direction

            samples.append(
                {name: float(current[i]) for i, name in enumerate(rxn_names)}
            )

        return samples

    def get_flux_range(self, reaction_name: str) -> dict:
        """Get the min/max flux range for a reaction from FVA.

        Args:
            reaction_name: Name of the reaction.

        Returns:
            Dict with 'min' and 'max' keys.

        Raises:
            ValueError: If reaction_name is not found.
        """
        if reaction_name not in self.reactions:
            raise ValueError(f"Reaction '{reaction_name}' not found")
        fva_result = self.fva()
        return fva_result[reaction_name]

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
