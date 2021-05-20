from panda3d.core import Vec3
# File: B (Python 2.4)

from direct.showbase import PythonUtil
TARGET_POS = {
    4: Vec3(0.848, 0, 0.0),
    3: Vec3(0.598, 0, 0.418),
    2: Vec3(0.27, 0, 0.598),
    1: Vec3(-0.08, 0, 0.63),
    0: Vec3(-0.58, 0, 0.288) }
FACES = PythonUtil.Enum('DEALER,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN')
FACE_SPOT_POS = {
    FACES.DEALER: (-1.0, 0, 0.598),
    FACES.ONE: (-1.14, 0, -0.299),
    FACES.TWO: (-0.956, 0, -0.609),
    FACES.THREE: (-0.65, 0, -0.800000),
    FACES.FOUR: (0.65, 0, -0.800000),
    FACES.FIVE: (0.956, 0, -0.609),
    FACES.SIX: (1.14, 0, -0.299) }
FINGER_RANGES = [
    [
        -26,
        -16],
    [
        -3,
        8],
    [
        23,
        32],
    [
        52,
        60]]
PLAYER_ACTIONS = PythonUtil.Enum('JoinGame,UnjoinGame,RejoinGame,Resign,Leave,Continue,Progress')
GAME_ACTIONS = PythonUtil.Enum('AskForContinue,NotifyOfWin,NotifyOfLoss')
CONTINUE_OPTIONS = PythonUtil.Enum('Resign,Continue,Rejoin,Leave')
GameTimeDelay = 5
RoundTimeDelay = 5
RoundTimeLimit = 90
RoundContinueWait = 10
