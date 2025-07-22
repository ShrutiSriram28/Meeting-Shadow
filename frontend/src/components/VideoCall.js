import React, { useEffect, useRef, useState } from "react";
import DailyIframe from "@daily-co/daily-js";
import { uploadAudio } from "../api";

export default function VideoCall({ onAiUpdate }) {
  const callContainerRef = useRef(null);
  const callFrameRef = useRef(null);
  const [recordingChunks, setRecordingChunks] = useState([]);
  const recordingChunksRef = useRef([]); 
  const mediaRecorderRef = useRef(null);

  useEffect(() => {
    if (callFrameRef.current) {
      callFrameRef.current.destroy();
      callFrameRef.current = null;
    }

    if (callContainerRef.current) {
      callFrameRef.current = DailyIframe.createFrame(callContainerRef.current, {
        iframeStyle: {
          width: "100%",
          height: "400px",
          border: "1px solid #ccc",
        },
      });

      callFrameRef.current.join({
        url: "https://aishadow.daily.co/test-room",
      });

      startAudioCapture();
    }

    return () => {
      if (callFrameRef.current) {
        console.log("Cleaning up Daily frame...");
        callFrameRef.current.destroy();
        callFrameRef.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const startAudioCapture = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      mediaRecorderRef.current = new MediaRecorder(stream, {
        mimeType: "audio/webm",
      });

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setRecordingChunks((prev) => {
            const updated = [...prev, event.data];
            recordingChunksRef.current = updated; 
            return updated;
          });
        }
      };

      mediaRecorderRef.current.start(3000);

      setInterval(() => {
        if (recordingChunksRef.current.length > 0) {
          sendChunkToBackend();
        }
      }, 5000);
    } catch (err) {
      console.error("Microphone error:", err);
    }
  };

  const sendChunkToBackend = async () => {
    const chunksToSend = recordingChunksRef.current;

    if (chunksToSend.length === 0) {
      return;
    }

    const audioBlob = new Blob(chunksToSend, { type: "audio/webm" });

    try {
      const result = await uploadAudio(audioBlob);
      onAiUpdate(result);
    } catch (err) {
      console.error("Error uploading audio:", err);
    } finally {
      setRecordingChunks([]);
      recordingChunksRef.current = [];
    }
  };

  return (
    <div
      ref={callContainerRef}
      >
    
    </div>
  );
}
