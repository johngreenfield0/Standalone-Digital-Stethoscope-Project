# Standalone-Digital-Stethoscope-Project
Files containing working AI model and CAD STL files 

"""
def rdlinet_predict_pro(audio_file_path):
    # 1. Load Model and Labels
    model_inference = tf.keras.models.load_model('/content/drive/MyDrive/Colab_Notebooks/RDLINet_8class_final.keras', compile=False)
    with open('/content/drive/MyDrive/Colab_Notebooks/RDLINet_LabelEncoder.pkl', 'rb') as f:
        classes = pickle.load(f)

    # 2. Extract Features (match training specs)
    y, sr = librosa.load(audio_file_path, sr=16000)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=64)
    mel_db = librosa.power_to_db(mel, ref=np.max)

    # Padding/Truncating to 300
    if mel_db.shape[1] < 300:
        feat = np.pad(mel_db, ((0,0), (0, 300 - mel_db.shape[1])), mode='constant')
    else:
        feat = mel_db[:, :300]

    # 3. Predict
    feat_input = feat.reshape(1, 64, 300, 1)
    preds = model_inference.predict(feat_input, verbose=0)

    # 4. Results
    res_idx = np.argmax(preds)
    print(f"\nTarget: {os.path.basename(audio_file_path)}")
    print(f"Result: {classes[res_idx]} ({np.max(preds)*100:.2f}% confidence)")

    return classes[res_idx] """
