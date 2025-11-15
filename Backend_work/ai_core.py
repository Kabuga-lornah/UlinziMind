import random
import time
from typing import List, Dict
import numpy as np 
import os
import math # For mathematical operations in fusion logic

# --- Core AI Dependencies ---
try:
    # Computer Vision (YOLOv8)
    from ultralytics import YOLO 
    # Natural Language Processing (BERT-based Hugging Face pipeline)
    from transformers import pipeline
except ImportError as e:
    # This block ensures the code runs even if heavy AI packages aren't installed yet.
    print(f"Warning: AI dependencies not found. Using stub classes. Error: {e}")
    YOLO = None
    pipeline = None

# --- 1. Computer Vision (Geospatial Intelligence) - YOLOv8 Integration ---

class GeospatialSentinel:
    """
    Integrates the YOLOv8 Computer Vision pipeline for object detection in satellite imagery.
    """
    def __init__(self):
        self.model = None
        if YOLO:
            try:
                # Load the smallest, fastest YOLOv8 model for demonstration (yolov8n.pt)
                self.model = YOLO('yolov8n.pt') 
                print("GeospatialSentinel: Loaded YOLOv8n model.")
            except Exception as e:
                print(f"Error loading YOLOv8n model. Falling back to random stub. Details: {e}")

    def process_satellite_imagery(self, image_metadata: Dict) -> Dict:
        """
        Runs object detection to quantify physical threats.
        """
        if self.model:
            # Placeholder for a sample image that YOLO can detect (e.g., people, vehicles)
            # In production, this would be a local path to a downloaded satellite image tile.
            image_source = 'https://ultralytics.com/images/bus.jpg' # Example URL with high object count
            
            # Run inference
            # imgsz=320 is used for faster, lower-resolution inference suitable for a dashboard API
            results = self.model.predict(source=image_source, imgsz=320, conf=0.25, verbose=False)
            
            # Extract results
            detected_objects = len(results[0].boxes) 
            
            # Simple logic to determine threat level based on object count
            if detected_objects > 8:
                threat_type = "Large Assembly Detected"
                # Calculate threat level, capping at 1.0
                threat_level = min(1.0, 0.6 + detected_objects * 0.04) 
            elif detected_objects > 3:
                threat_type = "Multiple Vehicles/People Detected"
                threat_level = 0.45
            else:
                threat_type = "Low Object Count"
                threat_level = 0.2
            
            return {
                "cv_threat_level": round(threat_level, 2),
                "cv_threat_type": threat_type,
                "detected_objects": detected_objects,
                "geo_coordinates": (image_metadata.get('latitude'), image_metadata.get('longitude'))
            }
        else:
            # Fallback (Stub Logic)
            threat_level = random.uniform(0.1, 0.9)
            detected_objects = random.randint(0, 15)
            threat_type = random.choice(["Illegal Gathering (Stub)", "Unregistered Vehicle Convoy (Stub)", "Normal Activity (Stub)"])
            
            return {
                "cv_threat_level": round(threat_level, 2),
                "cv_threat_type": threat_type,
                "detected_objects": detected_objects,
                "geo_coordinates": (image_metadata.get('latitude'), image_metadata.get('longitude'))
            }


# --- 2. NLP (Social Intelligence) - BERT Integration ---

class SocialSentinel:
    """
    Integrates the BERT-based NLP pipeline to analyze social media text for sentiment/threat.
    """
    def __init__(self):
        self.nlp_pipeline = None
        if pipeline:
            try:
                # Use a specific BERT-based model fine-tuned for sentiment analysis (Fast & Effective)
                self.nlp_pipeline = pipeline("sentiment-analysis", 
                                             model="finiteautomata/bertweet-base-sentiment-analysis")
                print("SocialSentinel: Loaded Hugging Face BERT-based model.")
            except Exception as e:
                print(f"Error loading NLP model. Falling back to random stub. Details: {e}")

    def analyze_social_stream(self, keywords: List[str]) -> Dict:
        """
        Analyzes a synthetic social media post based on keywords to gauge digital unrest.
        """
        # A simple model for generating a sample text based on input keywords
        if 'unrest' in keywords or 'protest' in keywords or 'shout' in keywords:
            sample_text = "The crowd is gathering near the main square, things are tense and people are shouting about the new policy. #KenyaProtest"
        elif 'violence' in keywords or 'hate' in keywords:
             sample_text = "They are spreading lies and calling for violence. The disinformation is dangerous! #Misinfo"
        else:
            sample_text = "Beautiful day in Nairobi, enjoying the market and the sun. Hope for peace."
            
        # print(f"-> Analyzing post: '{sample_text[:40]}...'")

        if self.nlp_pipeline:
            # Run inference
            result = self.nlp_pipeline(sample_text)[0]
            label = result['label']
            score = result['score']
            
            # Convert BERT sentiment into a digital threat index
            if label == 'NEG':
                sentiment_score = score
                digital_threat = "Growing Protest Discussion"
                misinformation_index = random.uniform(0.3, 0.7)
            elif label == 'NEU':
                sentiment_score = 0.0
                digital_threat = "Normal Digital Noise"
                misinformation_index = random.uniform(0.0, 0.1)
            else: # POS
                sentiment_score = 0.0 
                digital_threat = "Low Conflict Risk"
                misinformation_index = random.uniform(0.0, 0.1)
                
            return {
                "nlp_sentiment_score": round(sentiment_score, 2),
                "nlp_misinfo_index": round(misinformation_index, 2),
                "nlp_digital_threat": digital_threat
            }
        else:
            # Fallback (Stub Logic)
            sentiment_score = random.uniform(-0.9, 0.9)
            misinformation_index = random.uniform(0.0, 1.0)
            
            if sentiment_score < -0.5 and misinformation_index > 0.6:
                digital_threat = "High Incitement/Hate Speech (Stub)"
            else:
                digital_threat = "Normal Digital Noise (Stub)"
                
            return {
                "nlp_sentiment_score": round(sentiment_score, 2),
                "nlp_misinfo_index": round(misinformation_index, 2),
                "nlp_digital_threat": digital_threat
            }

# --- 3. GNN Fusion and Prediction Logic ---

class UlinziMindEngine:
    """
    Simulates the Graph Neural Network (GNN) fusion engine and ethical prediction module.
    
    NOTE: The fusion logic here is still based on simple rules, mimicking the output 
    a complex GNN would provide.
    """
    def __init__(self):
        # Initialize the two sentinel models
        self.geo_sentinel = GeospatialSentinel()
        self.social_sentinel = SocialSentinel()
        print("UlinziMindEngine: Initialized Core Fusion Engine.")

    def fuse_and_predict(self, geo_data: Dict, social_data: Dict) -> Dict:
        """
        Combines insights from physical (CV) and digital (NLP) streams 
        to produce a final, unified Security Alert.
        """
        # Extract key threat factors
        cv_level = geo_data['cv_threat_level']
        nlp_risk_score = social_data['nlp_sentiment_score'] # This is the NEG score from BERT
        misinfo_index = social_data['nlp_misinfo_index']
        detected_objects = geo_data['detected_objects']

        # --- CORE FUSION LOGIC (Rule-based mimicry of GNN) ---
        
        # Base risk is a weighted average of physical and digital risk
        unified_risk = (cv_level * 0.5) + (nlp_risk_score * 0.4) + (misinfo_index * 0.1)
        unified_risk = min(1.0, unified_risk) # Cap at 1.0

        # --- Ethical Design (Civic Peace Module) Logic ---
        # Peaceful Assembly = High detected objects but low risk/misinformation score
        is_peaceful = (detected_objects >= 3) and (misinfo_index < 0.2) and (nlp_risk_score < 0.3)
        
        # Determine Threat Type and Recommended Action
        if unified_risk > 0.8:
            threat = "CRITICAL: Coordinated Threat"
            action = "Immediate deployment and verification of source data."
        elif unified_risk > 0.6:
            threat = "HIGH: Escalating Unrest/Infiltration"
            action = "Implement non-violent crowd management protocols and communication."
        elif is_peaceful and detected_objects >= 3:
            threat = "MODERATE: Peaceful Civic Protest"
            # Overwrite the action to align with ethical design
            action = "Monitor only. Alert Amnesty Kenya/Red Cross for oversight."
            unified_risk = max(0.4, min(0.6, unified_risk)) # Cap risk for peaceful assembly
        elif misinfo_index > 0.7:
             threat = "HIGH: Misinformation Campaign"
             action = "Issue public advisory and engage civic organizations to counter misinformation."
        else:
            threat = "LOW: General Monitoring"
            action = "Routine surveillance and data logging."

        return {
            "risk_score": round(unified_risk, 2),
            "threat_type": threat,
            "source_type": "Satellite + Social (GNN Fusion)",
            "recommended_action": action,
            "peace_module_flag": is_peaceful
        }