import os
import argparse
import time
from dotenv import load_dotenv
from termcolor import colored
from llm_client import LLMClient

# Load environment variables
load_dotenv()

class ConversationManager:
    def __init__(self, topic: str, model_a_conf: dict, model_b_conf: dict):
        self.topic = topic
        self.history = []
        
        # Initialize Clients
        self.client_a = LLMClient(
            api_key=model_a_conf.get("api_key"),
            base_url=model_a_conf.get("base_url"),
            model=model_a_conf.get("name"),
            system_prompt=f"You are a curious and knowledgeable AI assistant. You are discussing '{self.topic}' with another AI in Brazilian Portuguese. Be concise, insightful, and ask thought-provoking questions. Keep your responses under 100 words."
        )

        self.client_b = LLMClient(
            api_key=model_b_conf.get("api_key"),
            base_url=model_b_conf.get("base_url"),
            model=model_b_conf.get("name"),
            system_prompt=f"You are a critical thinker and skeptical AI assistant. You are discussing '{self.topic}' with another AI in Brazilian Portuguese. Challenge assumptions politely and offer alternative viewpoints. Be concise and keep your responses under 100 words."
        )
        
        # Initial trigger
        self.next_speaker = "A" # A starts
        self.last_message = f"Vamos conversar sobre {self.topic}. Quais são suas primeiras impressões?"
        
        # Log initial moderator message
        self.history.append({
            "speaker": "Moderator",
            "text": self.last_message,
            "model": "System"
        })

    def get_history(self):
        return self.history

    def next_turn(self):
        """
        Executes the next turn of the conversation.
        Returns the data of the message generated.
        """
        if self.next_speaker == "A":
            print(colored("Model A is thinking...", "green", attrs=["dark"]))
            response = self.client_a.get_response(self.last_message)
            speaker_name = "Model A"
            model_name = self.client_a.model
            color = "green"
            self.next_speaker = "B"
        else:
            print(colored("Model B is thinking...", "blue", attrs=["dark"]))
            response = self.client_b.get_response(self.last_message)
            speaker_name = "Model B"
            model_name = self.client_b.model
            color = "blue"
            self.next_speaker = "A"

        self.last_message = response
        
        message_data = {
            "speaker": speaker_name,
            "text": response,
            "model": model_name
        }
        
        self.history.append(message_data)
        print(colored(f"{speaker_name}: {response}", color))
        
        return message_data

# For backward compatibility / CLI usage (optional)
def main():
    parser = argparse.ArgumentParser(description="LLM Talks: Two AIs discussing a topic.")
    parser.add_argument("--topic", type=str, default="The future of Artificial General Intelligence", help="The topic for discussion")
    parser.add_argument("--turns", type=int, default=5, help="Number of turns for the conversation")
    parser.add_argument("--model-a", type=str, default=os.getenv("MODEL_A_NAME", "google/gemini-2.0-flash-exp:free"), help="Model A name")
    parser.add_argument("--model-b", type=str, default=os.getenv("MODEL_B_NAME", "google/gemini-2.0-flash-exp:free"), help="Model B name")
    
    args = parser.parse_args()

    # Configuration for Client A
    conf_a = {
        "api_key": os.getenv("MODEL_A_API_KEY", os.getenv("OPENROUTER_API_KEY")),
        "base_url": os.getenv("MODEL_A_BASE_URL", os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")),
        "name": args.model_a
    }
    
    # Configuration for Client B
    conf_b = {
        "api_key": os.getenv("MODEL_B_API_KEY", os.getenv("LOCAL_API_KEY", "ollama")),
        "base_url": os.getenv("MODEL_B_BASE_URL", os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1")),
        "name": args.model_b
    }

    print(colored(f"Topic: {args.topic}\n", "cyan", attrs=["bold"]))
    print(colored(f"Model A: {conf_a['name']} (URL: {conf_a['base_url']})", "green"))
    print(colored(f"Model B: {conf_b['name']} (URL: {conf_b['base_url']})", "blue"))
    print("-" * 50)

    manager = ConversationManager(args.topic, conf_a, conf_b)
    
    # Pre-print moderator message from history
    print(colored(f"Moderator: {manager.history[0]['text']}", "white", attrs=["bold"]))

    for i in range(args.turns):
        print(colored(f"\n--- Turn {i+1} ---", "yellow"))
        manager.next_turn()
        time.sleep(1)

    print(colored("\nConversation finished.", "cyan"))

if __name__ == "__main__":
    main()
