import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

df = pd.read_excel('ECU_IoHT.xlsx') #veri setini yükle

# 1. VERİ ÖNİŞLEME
# 1.1 NULL değer olup olmadığını kontrol et
#print(df.isnull().sum()) 
#df = df.dropna()  # NULL değer bulunana satırları çıkar
# df = df.fillna(df.median()) # boş değerleri sütunun medyanı ile doldur

# 1.2 eğitimde kullanılmayacak sütünları çıkar
df = df.drop(columns=['No.', 'Time', 'Info']) 

# print("Before normalization:")
# print(df.head())

# 1.3 ketegorik verileri etiketle (label encoding)
label_encoder = LabelEncoder()
df['Source'] = label_encoder.fit_transform(df['Source'])
df['Destination'] = label_encoder.fit_transform(df['Destination'])
df['Protocol'] = label_encoder.fit_transform(df['Protocol'])
df['Type of attack'] = label_encoder.fit_transform(df['Type of attack'])
df['Type'] = label_encoder.fit_transform(df['Type'])

# 1.4 normalizasyon 
numerical_columns = df.drop(columns=['Type of attack']).select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# print("After normalization:")
# print(df.head())

# 1.5 veriyi özellik ve hedef (feature-target) diye ayır
y = df['Type of attack'] #hedef
x = df.drop(columns=['Type of attack']) #özellikler

# 1.6 eğitim ve test verisini ayır
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42) # 10% test 90% eğitim 

# 2. MODEL EĞİTİMİ
mlp_model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=52) #modeli oluştur
mlp_model.fit(x_train, y_train) #modeli eğitim verisiyle eğit
accuracy = mlp_model.score(x_test, y_test) #test verisiyle sınıflandırma yap

print(f'Model Accuracy: {accuracy * 100:.2f}%')

#confusion matrisi oluştur
y_pred = mlp_model.predict(x_test) 
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)


class_report = classification_report(y_test, y_pred)
print("Classification Report:")
print(class_report)

# Plot the loss curve
plt.plot(mlp_model.loss_curve_, label='Training Loss')
plt.title('Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# print("Unique values in y_test:", y_test.unique())
# print("Classes in label_encoder:", label_encoder.classes_)
