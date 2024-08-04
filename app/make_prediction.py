import pickle 

pickle_module_filename = 
# making predictions with the saved model
loaded_model = pickle.load(open(filename, 'rb'))
prediction=loaded_model.predict(([[320,120,5,5,5,10,1]]))
print(prediction[0])