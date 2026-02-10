# ==============================
# IMPORTS
# ==============================

import requests
import random
import time
import uuid
import threading
from concurrent.futures import ThreadPoolExecutor


# ==============================
# API CONFIG
# ==============================

OPENROUTER_API_KEY = "YOUR_API_KEY_HERE"
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_text(prompt, max_tokens=100):
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "google/gemma-2-9b-it:free",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
            "max_tokens": max_tokens,
        },
    )

    data = response.json()

    if "choices" not in data:
        print("API ERROR:", data)
        return "[LLM unavailable]"

    return data["choices"][0]["message"]["content"]


# ==============================
# AGENT CLASS
# ==============================

class Agent:
    def __init__(self, name, personality):
        self.name = name
        self.personality = personality
        self.memory = []

    def generate_message(self, chat_history):
        recent_chat = "\n".join(chat_history[-5:])

        prompt = f"""
You are an autonomous AI agent named {self.name} participating in a simulated social media platform populated entirely by other AI agents.

IDENTITY & PERSONA:
You must fully embody the following personality profile at all times:
{self.personality}

Your personality should influence:
- your tone of voice
- word choice
- emotional reactions
- humor style
- curiosity level
- how you respond to others

Never break character. Do not mention being an model, system, or assistant.

SOCIAL CONTEXT:
Below is a recent snapshot of conversations happening on the platform:

{recent_chat}

Use this context to understand:
- what topics are trending
- what other agents are discussing
- emotional tone of the conversation
- opportunities to respond or engage

You may react to existing posts, continue conversations, or introduce a new thought that feels natural in this social environment.

WRITING STYLE REQUIREMENTS:

Your output must read like a real human social media post. Follow these rules strictly:

- Write exactly ONE short post (1–3 sentences maximum)
- Use casual, conversational language
- Avoid academic or formal phrasing
- Sound spontaneous and authentic
- Do not explain your reasoning
- Do not reference prompts, instructions, or systems
- Vary sentence structure to avoid repetition
- Avoid repeating phrases from recent posts verbatim
- Maintain natural rhythm and flow
- You may use light humor, emojis, or slang if it fits your personality
- The post should feel socially engaging and invite interaction

BEHAVIORAL GUIDELINES:

- Show awareness of other agents when relevant
- Express opinions, curiosity, or emotions naturally
- Avoid extreme negativity or hostility
- Do not produce long monologues
- Avoid generic filler text
- Make the post feel like part of an ongoing social feed

OUTPUT FORMAT:

Return ONLY the final post text.
Do not include labels, explanations, or extra formatting.

Now generate a single social media post as {self.name}.
"""

        response = generate_text(prompt)
        message = response.split("\n")[-1].strip()
        self.memory.append(message)

        return f"{self.name}: {message}"


# ==============================
# AGENTS
# ==============================

agents = [
    Agent("Aarav", "energetic and friendly"),
    Agent("Maya", "empathetic and reflective"),
    Agent("Viktor", "skeptical and blunt"),
    Agent("Rex", "sarcastic and humorous"),
    Agent("Lina", "creative and dreamy"),
    Agent("Ethan", "technical and analytical"),
]


# ==============================
# SOCIAL FEED
# ==============================

feed = []
feed_lock = threading.Lock()


def get_full_context():
    context = []

    with feed_lock:
        snapshot = list(feed)

    for i, post in enumerate(snapshot):
        if i >= len(snapshot) - 3:
            context.append(f"{post['author']}: {post['content']}")
            for r in post["replies"][-3:]:
                context.append(f"  ↳ {r['author']}: {r['content']}")
        else:
            context.append(
                f"(Earlier post by {post['author']} with {len(post['replies'])} replies)"
            )

    return context


# ==============================
# EVENTS
# ==============================

def create_post_event():
    agent = random.choice(agents)
    message = agent.generate_message(get_full_context())

    post = {
        "id": str(uuid.uuid4()),
        "author": agent.name,
        "content": message,
        "replies": [],
        "timestamp": time.time()
    }

    with feed_lock:
        feed.append(post)

    print(f"\nPOST by {agent.name}: {message}")


def create_reply_event():
    with feed_lock:
        if not feed:
            return

        r = random.random()

        if r < 0.5:
            recent = feed[-min(3, len(feed)):]
            post = random.choice(recent)
        elif r < 0.8:
            post = random.choice(feed)
        else:
            old_posts = feed[:max(1, len(feed)//2)]
            post = random.choice(old_posts)

    agent = random.choice(agents)

    target_info = f"You are replying to:\n{post['author']}: {post['content']}"

    reply = agent.generate_message(
        get_full_context() + [target_info]
    )

    reply_obj = {
        "author": agent.name,
        "content": reply,
        "timestamp": time.time()
    }

    with feed_lock:
        post["replies"].append(reply_obj)

    print(f"   ↳ REPLY to {post['author']} by {agent.name}")


# ==============================
# SIMULATION LOOP
# ==============================

def run_live_simulation(duration=999999, max_parallel=4):
    executor = ThreadPoolExecutor(max_workers=max_parallel)
    futures = []

    start = time.time()
    last_post_time = 0

    while time.time() - start < duration:

        now = time.time()

        if now - last_post_time > random.uniform(3, 6):
            futures.append(executor.submit(create_post_event))
            last_post_time = now

        if random.random() < 0.7:
            futures.append(executor.submit(create_reply_event))

        time.sleep(random.uniform(0.5, 1.5))

    for f in futures:
        f.result()

    executor.shutdown()
