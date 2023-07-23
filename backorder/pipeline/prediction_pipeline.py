# import sys, os
# from backorder.logger import logging
# from backorder.exception import CustomException

# from backorder.utils import load_object
# import pandas as pd


# class PredictPipeline:
#     def __init__(self):
#         pass

#     def predict(self, features):
#         try:
#             preprocessor_file_path = os.path.join("artifacts", "preprocessor.pkl")
#             model_file_path = os.path.join("artifacts", "model.pkl")
#             logging.info("before loading")
            
#             preprocessor = load_object(file=preprocessor_file_path)
#             model = load_object(file=model_file_path)
#             logging.info("after loading")

#             data_scaled = preprocessor.transform(features)
#             pred = model.predict(data_scaled)
#             return pred
        
#         except Exception as e:
#             raise CustomException(e, sys)

# class CustomData:
#     def __init__(self,
#                 national_inv, lead_time, in_transit_qty, forecast_3_month, forecast_6_month,
#                 forecast_9_month, sales_1_month, sales_3_month, sales_6_month, sales_9_month, 
#                 min_bank, pieces_past_due, perf_6_month_avg, perf_12_month_avg, local_bo_qty,
#                 potential_issue, deck_risk, oe_constraint, ppap_risk, stop_auto_buy, rev_stop):
        
#         self.national_inv:float = national_inv
#         self.lead_time:float = lead_time
#         self.in_transit_qty:float = in_transit_qty
#         self.forecast_3_month:float = forecast_3_month
#         self.forecast_6_month:float = forecast_6_month
#         self.forecast_9_month:float = forecast_9_month
#         self.sales_1_month:float = sales_1_month
#         self.sales_3_month:float = sales_3_month
#         self.sales_6_month:float = sales_6_month
#         self.sales_9_month:float = sales_9_month
#         self.min_bank:float = min_bank
#         self.pieces_past_due:float = pieces_past_due
#         self.perf_6_month_avg:float = perf_6_month_avg
#         self.perf_12_month_avg:float = perf_12_month_avg
#         self.local_bo_qty:float = local_bo_qty
        
#         self.potential_issue:str = potential_issue
#         self.deck_risk:str = deck_risk
#         self.oe_constraint:str = oe_constraint
#         self.ppap_risk:str = ppap_risk
#         self.stop_auto_buy:str = stop_auto_buy
#         self.rev_stop:str = rev_stop

#     def get_data_as_data_frame(self):
#         try:
#             custom_data_input:dict = {
#                 'national_inv':[self.national_inv],
#                 'lead_time':[self.lead_time],
#                 'in_transit_qty':[self.in_transit_qty],
#                 'forecast_3_month':[self.forecast_3_month],
#                 'forecast_6_month':[self.forecast_6_month],
#                 'forecast_9_month':[self.forecast_9_month],
#                 'sales_1_month':[self.sales_1_month],
#                 'sales_3_month':[self.sales_3_month],
#                 'sales_6_month':[self.sales_6_month],
#                 'sales_9_month':[self.sales_9_month],
#                 'min_bank':[self.min_bank],
#                 'pieces_past_due':[self.pieces_past_due],
#                 'perf_6_month_avg':[self.perf_6_month_avg],
#                 'perf_12_month_avg':[self.perf_12_month_avg],
#                 'local_bo_qty':[self.local_bo_qty],
#                 'potential_issue':[self.potential_issue],
#                 'deck_risk':[self.deck_risk],
#                 'oe_constraint':[self.oe_constraint],
#                 'ppap_risk':[self.ppap_risk],
#                 'stop_auto_buy':[self.stop_auto_buy],
#                 'rev_stop':[self.rev_stop]
#             }

#             return pd.DataFrame(custom_data_input)
        
#         except Exception as e:
#             raise CustomException(e, sys)
