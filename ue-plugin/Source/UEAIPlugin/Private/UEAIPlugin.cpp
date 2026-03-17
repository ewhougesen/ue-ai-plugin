// Copyright Epic Games, Inc. All Rights Reserved.

#include "UEAIPlugin.h"
#include "UEAIPluginSettings.h"
#include "UEAIService.h"
#include "UEAIEditorWidget.h"
#include "LevelEditor.h"
#include "Widgets/Docking/SDockTab.h"
#include "ToolMenus.h"
#include "Styling/AppStyle.h"
#include "Framework/Commands/UICommandList.h"
#include "Framework/Commands/UICommandInfo.h"
#include "Framework/MultiBox/MultiBoxBuilder.h"
#include "Framework/MultiBox/MultiBoxExtender.h"

#define LOCTEXT_NAMESPACE "FUEAIPluginModule"

static const FString UEAIPluginTabName = TEXT("UEAIPlugin");

// Command list
TSharedPtr<FUICommandList> FUEAIPluginModule::PluginCommands;

void FUEAIPluginModule::StartupModule()
{
    // Initialize command list
    PluginCommands = MakeShareable(new FUICommandList);

    // Initialize settings
    UUEAIPluginSettings::RegisterSettings();

    // Initialize the AI service
    FUEAIService::Get().Initialize();

    // Register editor extensions
    RegisterEditorExtensions();

    UE_LOG(LogUEAIPlugin, Log, TEXT("UE AI Plugin started successfully"));
}

void FUEAIPluginModule::ShutdownModule()
{
    // Unregister editor extensions
    UnregisterEditorExtensions();

    // Shutdown the AI service
    FUEAIService::Get().Shutdown();

    UE_LOG(LogUEAIPlugin, Log, TEXT("UE AI Plugin shut down"));
}

void FUEAIPluginModule::RegisterEditorExtensions()
{
    // Register menu extension
    if (UToolMenus* ToolMenus = UToolMenus::Get())
    {
        UToolMenu* Menu = ToolMenus->ExtendMenu("LevelEditor.MainMenu.Window");
        FToolMenuSection& Section = Menu->AddSection("WindowAI", FText::FromString("AI"), FToolMenuInsertByName("WindowLayout", EToolMenuInsertType::After));

        {
            FToolMenuEntry& Entry = Section.AddEntry(
                FToolMenuEntry::InitMenuEntry(
                    FName("UEAIPluginTab"),
                    FText::FromString("UE AI Plugin"),
                    FText::FromString("Open the UE AI Plugin panel"),
                    FSlateIcon(FAppStyle::GetAppStyleSetName(), "Icons.Person"),
                    FUIAction(
                        FExecuteAction::CreateLambda([]()
                        {
                            FGlobalTabmanager::Get()->TryInvokeTab(FName(*UEAIPluginTabName));
                        }),
                        FCanExecuteAction()
                    )
                )
            );
            Entry.SetCommandList(PluginCommands);
        }
    }

    // Register tab spawner
    FGlobalTabmanager::Get()->RegisterNomadTabSpawner(
        FName(*UEAIPluginTabName),
        FOnSpawnTab::CreateStatic(&SUEAIEditorWidget::SpawnTab)
    )
    .SetDisplayName(FText::FromString("UE AI Plugin"))
    .SetMenuType(ETabSpawnerMenuType::Hidden);
}

void FUEAIPluginModule::UnregisterEditorExtensions()
{
    if (UToolMenus* ToolMenus = UToolMenus::Get())
    {
        ToolMenus->UnregisterOwnerByName("UEAIPlugin");
    }

    FGlobalTabmanager::Get()->UnregisterNomadTabSpawner(FName(*UEAIPluginTabName));
}

FString FUEAIPluginModule::GetBackendServerURL()
{
    UUEAIPluginSettings* Settings = GetMutableDefault<UUEAIPluginSettings>();
    if (Settings)
    {
        return Settings->BackendServerURL;
    }
    return FString(TEXT("http://localhost:8000"));
}

bool FUEAIPluginModule::IsBackendConnected()
{
    return FUEAIService::Get().IsConnected();
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FUEAIPlugin, UEAIPlugin)
DEFINE_LOG_CATEGORY(LogUEAIPlugin);
TSharedPtr<FUICommandList> FUEAIPluginModule::PluginCommands = nullptr;
