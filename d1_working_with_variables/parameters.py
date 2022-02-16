parameters = {'calculate_congested_ivtt_flag': True, 'node_logit_scale': True, 'effective_headway_attribute': '@ehdw1', 'effective_headway_slope': 0.165, 'headway_fraction_attribute': '@frac1',
              'iterations': 100, 'norm_gap': 0, 'rel_gap': 0, 'scenario_number': 1, 'walk_speed': 0, 'transit_classes': [{'name': 'transit_class_1', 'board_penalty_matrix': 'mf0', 'board_penalty_perception': 1, 'congestion_matrix': 'mf0', 'demand_matrix': 'mf0', 'fare_matrix': 'mf0', 'fare_perception': 0, 'in_vehicle_time_matrix': 'mf0', 'impedance_matrix': 'mf0', 'link_fare_attribute_id': '@lfare1', 'mode': '*', 'perceived_travel_time_matrix': 'mf0', 'segment_fare_attribute': '@sfare1', 'wait_time_perception': 0, 'wait_time_matrix': 'mf0'
                                                                                                                          'walk_time_perception_attribute': '@walkp1'
                                                                                                                          'walk_time_matrix': 'mf0'
                                                                                                                          'walk_perceptions': [{'filter': 'i=10000,20000 or j=1...7000,98000', 'walk_perception_value': 1.8}]}], 'congestion_exponent': '', 'assignment_period': 0, 'name_string': ''}




"""
        This method creates a network that completely replaces the scenario network in memory/disk 
        with one that allows for the use of a logit distribution at specified choice points.

        - Runs only when the parameter "node_logit_scale" is not FALSE
        - If "node_logit_scale" is FALSE, the optimal strategy transit assignment option is used. However,
            
             the optimal strategy makes it difficult to :
                * keep track of and maintain choice model structure, alternatives, and utilities
                * compute the resulting choice probabilities and demand shares
        HOW?
        > FOR NODES: Here we use we use regular nodes that are centroids as our choice points
            *  set node attributes to -1 to apply logit to efficient connectors (ie. connectors that bring 
               travellers closer to the destination) only
               NOTE: 1 is used to apply to all connectors
        > FOR LINKS: Here we override the flow connectors with fixed proportions. For the connectors outgoing 
          from other origins, the link attribute must be set to −1.
          NOTE: Proportions can be provided only for a subset of origins; 
        """