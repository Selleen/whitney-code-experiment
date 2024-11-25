import random
from const import *
from engine import *

class StoryWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Story")
        self.geometry("400x300")
        self.text_display = tk.Text(self, wrap=tk.WORD, height=10, width=40)
        self.text_display.pack(padx=10, pady=10)
        
        self.show_button = tk.Button(self, text="Show history", command=self.show_story)
        self.show_button.pack(pady=10)

    def show_story(self):
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, "History started...\n")

    def draw(self):
        self.text_display.insert(tk.END, "Updated history...\n")
        
def main(story_window):
    story_window.after(1000, main_logic)
    story_window.mainloop()

def main_logic():
    
    if YourAttitude == CHAUVINIST:
        if Fetch(pail, jack, jill):
            GoUpHill(jack, jill)

        if FellDown(jack) and BrokeCrown(jack):
            TumblingAfter(jill, jack)

    elif YourAttitude == FEMINIST:
        if Fetch(pail, jill, jack):
            GoUpHill(jill, jack)

        if FellDown(jill) and BrokeCrown(jill):
            TumblingAfter(jack, jill)
    
    story_window.draw()
        
def GoUpHill(Leader, follower):
    if ChangeItIf(SLIM_CHANCE):
        if (Leader.EmotionalState == INDECISIVE or Leader.EmotionalState == RELUCTANT) and ChangeItIf(Leader.Desire):
            Leader.EmotionalState = WILLING
        elif (Leader.EmotionalState == INDECISIVE or Leader.EmotionalState == WILLING) and ChangeItIf(1 - Leader.Desire):
            Leader.EmotionalState = RELUCTANT
        elif (Leader.EmotionalState == RELUCTANT or Leader.EmotionalState == WILLING) and ChangeItIf(1 - follower.Desire):
            Leader.EmotionalState = INDECISIVE

    if ChangeItIf(follower.Desire) and Leader.EmotionalState != FALLING:
        follower.EmotionalState = Leader.EmotionalState

    if ChangeItIf(SMALL_CHANCE):
        if (follower.EmotionalState == INDECISIVE or follower.EmotionalState == RELUCTANT) and ChangeItIf(follower.Desire):
            follower.EmotionalState = WILLING
        elif (follower.EmotionalState == INDECISIVE or follower.EmotionalState == WILLING) and ChangeItIf(1 - follower.Desire):
            follower.EmotionalState = RELUCTANT
        elif (follower.EmotionalState == RELUCTANT or follower.EmotionalState == WILLING) and ChangeItIf(1 - Leader.Desire):
            Leader.EmotionalState = INDECISIVE

def Fetch(Goal, Leader, follower):
    if not hasattr(Fetch, "lastFetch"):
        Fetch.lastFetch = False

    if Leader.EmotionalState == TUMBLING:
        Fetch.lastFetch = False
    else:
        if ChangeItIf(SMALL_CHANCE):
            if ChangeItIf(Goal.Allure):
                Leader.EmotionalState = WILLING
                follower.EmotionalState = WILLING
                Fetch.lastFetch = True
            elif ChangeItIf(1 - Goal.Allure):
                Leader.EmotionalState = RELUCTANT
                follower.EmotionalState = RELUCTANT
                Fetch.lastFetch = False

    return Fetch.lastFetch

def FellDown(Leader):
    if not hasattr(FellDown, "lastFell"):
        FellDown.lastFell = False

    if Leader.direction == UP_HILL and Leader.position.X > TOP_OF_HILL and Leader.EmotionalState == RELUCTANT:
        FellDown.lastFell = True
        Leader.EmotionalState = FALLING
    else:
        FellDown.lastFell = False

    return FellDown.lastFell

def BrokeCrown(Leader):
    if not hasattr(BrokeCrown, "lastCrown"):
        BrokeCrown.lastCrown = False
    if Leader.EmotionalState == FALLING:
        if ChangeItIf(GOOD_CHANCE):
            Leader.EmotionalState = BROKE_CROWN
            BrokeCrown.lastCrown = True
    else:
        BrokeCrown.lastCrown = False

    return BrokeCrown.lastCrown

def TumblingAfter(follower, Leader):
    if Leader.EmotionalState == BROKE_CROWN:
        if ChangeItIf(GOOD_CHANCE):
            Leader.EmotionalState = TUMBLING
            follower.EmotionalState = INDECISIVE

def ChangeItIf(percent):
    return random.random() <= percent

if __name__ == "__main__":
    story_window = StoryWindow()
    main(story_window)