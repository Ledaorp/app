from flask import jsonify, render_template, Blueprint, request
from models import Lcd
from periphery import I2C
from app import send, set

BPmotorController = Blueprint("lcdController", __name__)

lcd =Lcd.LCD(0x27)