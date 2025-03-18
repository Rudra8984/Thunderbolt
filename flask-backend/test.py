from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid
from resume_processor import process_resume
from paper_retrieval import get_research_papers