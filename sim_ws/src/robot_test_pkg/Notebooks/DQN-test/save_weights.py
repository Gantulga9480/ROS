from keras.models import load_model

model=load_model('model_1.h5')
model.save_weights('model_1_weights.h5')
model=load_model('model_2.h5')
model.save_weights('model_2_weights.h5')

