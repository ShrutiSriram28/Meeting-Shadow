import axios from "axios"

const API_BASE = "http://127.0.0.1:5000"

export async function uploadAudio(audioBlob) {
    const formData = new FormData();
    formData.append("audio", audioBlob, "chunk.wav");

    const response = await axios.post(`${API_BASE}/upload_audio`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
    });

    return response.data;
}