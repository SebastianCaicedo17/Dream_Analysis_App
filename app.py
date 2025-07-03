import streamlit as st
from backend import audio_to_text, reve_analysis, ia_image
from PIL import Image
import os

st.set_page_config(page_title="Analyse de rêve IA", layout="centered")

st.title("Synthétiseur de rêves")

# Upload du fichier audio
uploaded_file = st.file_uploader("📤 Téléverse un fichier audio (.m4a)", type=["m4a"])

if uploaded_file is not None:
    with open("Audio.m4a", "wb") as f:
        f.write(uploaded_file.read())
    st.success("Fichier audio enregistré avec succès ✅")

    if st.button("🎧 Transcrire et analyser le rêve"):
        with st.spinner("Transcription en cours..."):
            texte = audio_to_text("Audio.m4a")
        st.text_area("📝 Texte transcrit :", texte, height=150)

        with st.spinner("Analyse du rêve en cours..."):
            resultats = reve_analysis(texte)
        st.subheader("🔍 Analyse émotionnelle")
        st.json(resultats)

        with st.spinner("Génération d'une image basée sur le rêve..."):
            ia_image(texte)

        # Affichage de l'image
        if os.path.exists("image_generée.png"):
            image = Image.open("image_generée.png")
            st.image(image, caption="🖼️ Image générée à partir du rêve")

            # Téléchargement
            with open("image_generée.png", "rb") as file:
                st.download_button(
                    label="📥 Télécharger l'image",
                    data=file,
                    file_name="image_reve.png",
                    mime="image/png"
                )
        else:
            st.error("❌ Erreur lors de la génération de l'image.")
