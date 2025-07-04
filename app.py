import streamlit as st
from backend import audio_to_text, reve_analysis, ia_image
from PIL import Image
from io import BytesIO
import os
import plotly.express as px

st.set_page_config(page_title="Analyse de rêve IA", layout="centered")

st.title("Synthétiseur de rêves")

# Upload du fichier audio
uploaded_file = st.file_uploader("📤 Téléverse un fichier audio (.m4a)", type=["m4a"])

if uploaded_file is not None:
    texte = audio_to_text(uploaded_file)
    st.text_area("Texte transcrit", texte, height=150)

    if st.button("🎧 Analyser le rêve"):
        with st.spinner("Transcription en cours..."):
            texte = audio_to_text(uploaded_file)

        with st.spinner("Analyse du rêve en cours..."):
            resultats = reve_analysis(texte)
        st.subheader("🔍 Analyse émotionnelle")
        
        filtered = {k: v for k, v in resultats.items() if v > 0}
        fig = px.pie(
            names=list(filtered.keys()),
            values=list(filtered.values()),
            title="Répartition des émotions dans le rêve",
            hole=0.3
        )

        st.plotly_chart(fig, use_container_width=True)
        

        with st.spinner("Génération d'une image basée sur le rêve..."):
           image = ia_image(texte)

        # Affichage de l'image
        if image:
            st.image(image, caption="🖼️ Image générée à partir du rêve")
            img_bytes = BytesIO()
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Téléchargement
            st.download_button(
                label="📥 Télécharger l'image",
                data=img_bytes,
                file_name="image_reve.png",
                mime="image/png"
            )
        else:
            st.error("❌ Erreur lors de la génération de l'image.")
