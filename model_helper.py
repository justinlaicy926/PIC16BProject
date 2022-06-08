def predict(num_prediction, model):
  """
  Takes in a model and a number for days to predict, outputs the predicted values
  """
  prediction_list = close_data[-look_back:]
  for _ in range(num_prediction):
      x = prediction_list[-look_back:]
      x = x.reshape((1, look_back, 1))
      out = model.predict(x)[0][0]
      prediction_list = np.append(prediction_list, out)
  prediction_list = prediction_list[look_back-1:]
  return prediction_list
    
def predict_dates(num_prediction):
  """
  Takes in the number of predictions and outputs the dates for these predictions based on previous data
  """
  last_date = df['Date'].values[-1]
  prediction_dates = pd.date_range(last_date, periods=num_prediction+1).tolist()
  return prediction_dates

  def datetime_to_timestamp(x):
    '''
        x : a given datetime value (datetime.date)
    '''
    return datetime.strptime(x.strftime('%Y%m%d'), '%Y%m%d')
