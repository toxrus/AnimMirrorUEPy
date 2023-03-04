# AnimMirrorUEPy
Simple python script to batch mirror animations in Unreal Engine Sequencer.
Tested on 5.1.1
How to use:
1. Create an empty level and drop in the SkeletalMeshActor you want to create mirrored animations for. 
2. Create a MirrorDataTable for the corresponding skeleton (Animation -> M<irror Data Table)
3. Create a LevelSequence (Left of play button above the default game viewport)
4. Put your original animations inside a folder (optional)
5. Create a folder to save the mirrored animations in (optional)
6. Inside the python file under def addSkeletalAnimationTrackOnActor() (line 28) change the following lines to match the names of your assets
    sequencesFolder_path = '/Game/ConvertAnimations/InputAnimations'
    outputFolder_path = '/Game/ConvertAnimations/OutputAnimations/'
    sequence_path = '/Game/ConvertAnimations/MirrorLevelSequence'
    mirrorData_path = '/Game/ConvertAnimations/DT_Mirror'
    animSuffix = '_Mirrored'
7. Enable the "Python Editor Script Plugin"
8. Make sure the level is open and visible in the active viewport -> Under Tools select "Execute Python Script ..."
9. Select MirrorAnimn.py. Check Output Log for completion message.
