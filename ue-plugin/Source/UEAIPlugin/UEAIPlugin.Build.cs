// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class UEAIPlugin : ModuleRules
{
    public UEAIPlugin(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicIncludePaths.AddRange(
            new string[] {
                // ... add public include paths required here ...
            }
        );


        PrivateIncludePaths.AddRange(
            new string[] {
                "UEAIPlugin/Private",
                // ... add other private include paths required here ...
            }
        );


        PublicDependencyModuleNames.AddRange(
            new string[]
            {
                "Core",
                "CoreUObject",
                "Engine",
                "InputCore",
                "HTTP",
                "Json",
                "JsonUtilities",
                "Slate",
                "SlateCore",
                "EditorStyle",
                "EditorWidgets",
                "UnrealEd",
                "ToolMenus",
                "PythonScriptPlugin",
                "LevelEditor",
                "AssetRegistry",
                "AssetTools",
                "KismetCompiler",
                "BlueprintGraph",
                "KismetWidgets",
                "ContentBrowser",
                "DesktopPlatform",
                "Projects",
                "EditorStyle",
                "Editor",
                "UMG",
                "UMGEditor",
                "ComponentVisualizers",
                "Components"
            }
        );


        PrivateDependencyModuleNames.AddRange(
            new string[]
            {
                // ... add private dependencies that you statically link in here ...
            }
        );


        DynamicallyLoadedModuleNames.AddRange(
            new string[]
            {
                // ... add any modules that your plugin loads dynamically here ...
            }
        );
    }
}
