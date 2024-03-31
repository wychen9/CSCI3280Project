import HomepageGUI
import EventHandler

eventHandler = EventHandler.EventHandler()
homepageGUI = HomepageGUI.HomepageGUI(eventHandler)
eventHandler.setHomepageGUI(homepageGUI)
homepageGUI.createGUI()
