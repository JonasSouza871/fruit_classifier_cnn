from tflite_runtime.interpreter import Interpreter
import numpy as np
from PIL import Image
import json

#Caminho do modelo e labels
model_path = "trained_model/modelo_fruits_compat.tflite"
labels_path = 'trained_model/labels_traduzidas.json'

#Carregar labels
with open(labels_path, 'r') as f:
    labels = json.load(f)

#Abrir o modelo em memória (sem mmap)
with open(model_path, 'rb') as f:
    model_content = f.read()
interpreter = Interpreter(model_content=model_content)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details() #abir modelo tflite
output_details = interpreter.get_output_details()

#imagem que voce predente analisar
image_path = 'images/maca.png'
#processamento imagem
img = Image.open(image_path).convert('RGB')
img = img.resize((100, 100))  # ajuste conforme o tamanho do modelo
img_array = np.array(img, dtype=np.float32) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Rodar predição apartir do modelo tflite treinado
interpreter.set_tensor(input_details[0]['index'], img_array)
interpreter.invoke()
predictions = interpreter.get_tensor(output_details[0]['index'])[0]

pred_class = np.argmax(predictions) #calcula visao apartir das label
confidence = predictions[pred_class] #confiança na previsão
print(f"\nPredição: {labels[str(pred_class)]}")
print(f"Confiança: {confidence*100:.2f}%")

# Top 3 predições
print("\nTop 3 predições:")
top3 = np.argsort(predictions)[-3:][::-1] #mostra apenas as 3 primeiras
for i, idx in enumerate(top3, 1):
    print(f"{i}. {labels[str(idx)]}: {predictions[idx]*100:.2f}%")
