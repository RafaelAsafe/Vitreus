import pickle


test_exam_filename = config.get('exame_teste')
pickle_module_filename = config.get('pickle_module_filename')

# making predictions with the saved model
loaded_model = pickle.load(open(filename, 'rb'))
prediction = loaded_model.predict((test_exam_filename))
print(prediction[0])
