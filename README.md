import random
import time
import os
from colorama import Fore, init

# Initialize colorama for colored text
init(autoreset=True)

# Define romantic message templates
MESSAGE_TEMPLATES = [
    "My dearest {name}, you are the {adjective} star in my sky. Every moment with you is a {noun} I'll cherish forever.",
    "Roses are red, violets are blue, {name}, my heart belongs only to you.",
    "To {name}: If love was time, I'd give you eternity. If love was a {noun}, I'd give you infinity.",
    "Every time I {verb}, I think of you. You're the {adjective} melody in my life's song, {name}.",
    "{name}, you're the {adjective} dream I never want to wake from. My love for you grows {adverb} each day.",
    "My {name}, you're the {noun} to my soul, the {noun} to my heart. I {verb} you more than words can say."
]

# Word banks for dynamic content
ADJECTIVES = ["brightest", "most beautiful", "guiding", "brilliant", "sparkling", "radiant"]
NOUNS = ["treasure", "blessing", "miracle", "adventure", "dream", "masterpiece"]
VERBS = ["breathe", "smile", "dream", "hope", "live", "shine"]
ADVERBS = ["stronger", "deeper", "more passionately", "endlessly", "exponentially"]

def generate_love_message(name):
    """Generate a personalized love message"""
    template = random.choice(MESSAGE_TEMPLATES)
    return template.format(
        name=name,
        adjective=random.choice(ADJECTIVES),
        noun=random.choice(NOUNS),
        verb=random.choice(VERBS),
        adverb=random.choice(ADVERBS)
    )

def display_hearts(message):
    """Display the message with heart animation"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print decorative hearts
    heart_top = "   ♥♥♥     ♥♥♥   "
    heart_row = " ♥     ♥ ♥     ♥ "
    heart_full = "♥         ♥       ♥"
    
    print(Fore.MAGENTA + heart_top.center(50))
    print(Fore.MAGENTA + heart_row.center(50))
    print(Fore.MAGENTA + heart_full.center(50))
    
    # Print the message in stages
    print("\n" + Fore.RED + "❤️ A Message From The Heart ❤️".center(50) + "\n")
    
    words = message.split()
    revealed_message = []
    
    for word in words:
        revealed_message.append(word)
        print(Fore.YELLOW + " ".join(revealed_message).center(50))
        time.sleep(0.3)
    
    # Final decorative border
    print(Fore.GREEN + "\n" + "~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~".center(50))
    print(Fore.CYAN + "Forever Yours,".center(50))
    print(Fore.BLUE + "Your Secret Admirer".center(50) + "\n")

def main():
    """Main program function"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + "\n" + "❤️ WELCOME TO THE LOVE MESSENGER ❤️".center(50))
    
    name = input("\n" + Fore.CYAN + "Enter your beloved's name: " + Fore.YELLOW)
    
    while True:
        message = generate_love_message(name)
        display_hearts(message)
        
        choice = input(Fore.MAGENTA + "Create another message? (y/n): " + Fore.WHITE).lower()
        if choice != 'y':
            print(Fore.GREEN + "\nMay your love shine forever! ❤️")
            break

if __name__ == "__main__":
    main()# Here are your Instructions
