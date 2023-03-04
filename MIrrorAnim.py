#import unreal API into unreal engine
import unreal


# sequence_path: str : Level sequence path
# actor : obj unreal.actor : Actor used to add mirror animation to (and mirror animation from)
# return : obj unreal.SequenceBindingProxy : Actor binding
def getOrAddPossessableInSequenceAsset(sequence_path='', actor = None):
    sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
    possessable = sequence_asset.add_possessable(object_to_possess = actor)
    return possessable,sequence_asset

# animation_path : str : animation asset path
# possessable : obj unreal.SequenceBindingProxy : Actor binding
def addSkeletalAnimationTrackOnPossessable(animation_path = '', possessable = None, mirrorData_asset = None):
    # Get animation
    animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
    params = unreal.MovieSceneSkeletalAnimationParams(mirror_data_table = mirrorData_asset)
    params.set_editor_property('Animation', animation_asset)
    # Add track
    animation_track = possessable.add_track(track_type=unreal.MovieSceneSkeletalAnimationTrack)
    # Add section
    animation_section = animation_track.add_section()
    animation_section.set_editor_property('Params', params)
    animation_section.set_range(0,animation_asset.get_editor_property('number_of_sampled_frames'))
    return animation_asset

def addSkeletalAnimationTrackOnActor():
    # paths to the various items. Changeable by user
    sequencesFolder_path = '/Game/ConvertAnimations/InputAnimations'
    outputFolder_path = '/Game/ConvertAnimations/OutputAnimations/'
    sequence_path = '/Game/ConvertAnimations/MirrorLevelSequence'
    mirrorData_path = '/Game/ConvertAnimations/DT_Mirror'
    animSuffix = '_Mirrored'


    # get the current open level
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    # get the skeletonMeshActor for which animations will be mirrored
    actor_in_world = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.SkeletalMeshActor)[0]
    # get the sequence
    possessable_in_sequence, sequence_asset = getOrAddPossessableInSequenceAsset(sequence_path, actor_in_world)
    asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_reg.get_assets_by_path(sequencesFolder_path)
    mirrorData_asset = unreal.load_asset(mirrorData_path)



    for asset in assets :
        full_name = asset.get_full_name()
        pathLong = full_name.split(' ')[-1]
        animation_path = pathLong.split('.')[0]
        nameToSave = pathLong.split('.')[-1] + animSuffix

        # clear old AnimationTracks
        unreal.SequencerTools.clear_linked_anim_sequences(sequence_asset)
        tracks = possessable_in_sequence.get_tracks()
        for track in tracks :
            possessable_in_sequence.remove_track(track)
        # Add the new AnimationTrack and save a reference to the original animation asset
        animation_asset = addSkeletalAnimationTrackOnPossessable(animation_path, possessable_in_sequence,mirrorData_asset)
        # fit the play range to the latest animation asset
        sequence_asset.set_playback_end(animation_asset.get_editor_property('number_of_sampled_frames'))


        # Create animation sequence export options
        anim_seq_export_options = unreal.AnimSeqExportOption()
        anim_seq_export_options.export_transforms = True
        anim_seq_export_options.export_morph_targets = True

        # Get asset tools
        # Create an empty AnimSequence - /Game/Test_Anim
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        anim_sequence = unreal.AssetTools.create_asset(asset_tools, asset_name = nameToSave, package_path = outputFolder_path,
                                                       asset_class=unreal.AnimSequence,
                                                       factory=unreal.AnimSequenceFactory())

        # Bake to the created AnimSequence
        unreal.SequencerTools.export_anim_sequence(world, sequence_asset, anim_sequence, anim_seq_export_options,
                                                   possessable_in_sequence, False)


# Run code
addSkeletalAnimationTrackOnActor()
unreal.LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()
print("Animation mirroring completed. Enjoy")
# unreal.SequencerTools.export_anim_sequence(world, sequence, anim_sequence, export_option, binding, create_link)
