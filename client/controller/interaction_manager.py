from state_machine.state_manager import StateManager, State
from api.server_api import send_text_to_server, reset_session, play_tts
from voice.voice_listener import VADVoiceListener
import time
import logging

logger = logging.getLogger(__name__)

class InteractionManager:
    def __init__(self, session_id="kiosk-session"):
        logging.debug("InteractionManager - Initialzied")
        self.session_id = session_id
        self.state = StateManager()
        self.voice_listener = VADVoiceListener()
        

    def run(self):
        self.state.set_state(State.START)

        while True:
            current_state = self.state.get_state()

            if current_state == State.START:
                logging.debug("🔄 Resetting session and greeting user...")
                reset_session(self.session_id)
                self.state.set_state(State.GREETING)

            elif current_state == State.GREETING:
                response = send_text_to_server("สวัสดี", self.session_id)
                self.handle_response(response)

            elif current_state == State.LISTENING:
                logging.info("🎧 Listening for user input...")
                user_text = self.voice_listener.listen_and_recognize()
                logging.info(f"user_text={user_text}")
                if user_text:
                    response = send_text_to_server(user_text, self.session_id)
                    self.handle_response(response)
                else:
                    logging.info("🤷 ไม่เข้าใจเสียงที่พูด ลองใหม่อีกครั้ง")

            elif current_state == State.CONFIRMING:
                logging.info("📋 สรุปออเดอร์และยืนยัน")
                user_text = self.voice_listener.listen_and_recognize()
                if user_text:
                    response = send_text_to_server(user_text, self.session_id)
                    self.handle_response(response)
                else:
                    logging.warning("❌ ไม่เข้าใจคำพูดในการยืนยัน")
                    self.state.set_state(State.LISTENING)  # หรือวนกลับให้ฟังใหม่

            elif current_state == State.THANK_YOU:
                logging.info("🙏 ขอบคุณลูกค้า")
                time.sleep(2)
                self.state.set_state(State.END)

            elif current_state == State.END:
                logging.info("🔁 กลับสู่การเริ่มต้นใหม่")
                self.state.set_state(State.START)

    def handle_response(self, response_json):
        if response_json is None:
            logging.error("❌ ไม่สามารถเชื่อมต่อกับ server หรือ server ไม่ตอบกลับ")
            self.state.set_state(State.LISTENING)
            return

        intent = response_json.get("intent")
        tts_url = response_json.get("tts_url")

        if tts_url:
            play_tts(tts_url)

        if intent == "greeting":
            self.state.set_state(State.LISTENING)

        elif intent == "add_order":
            self.state.set_state(State.LISTENING)

        elif intent == "confirm_order":
            self.state.set_state(State.CONFIRMING)

        elif intent == "cancel_order":
            self.state.set_state(State.START)

        elif intent == "thank_you":
            self.state.set_state(State.THANK_YOU)

        else:
            logging.warning(f"⚠️ ไม่รู้จัก intent: {intent}, default to LISTENING")
            self.state.set_state(State.LISTENING)