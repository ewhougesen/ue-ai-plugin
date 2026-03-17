// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Input/Reply.h"
#include "Widgets/SCompoundWidget.h"
#include "Widgets/DeclarativeSyntaxSupport.h"

class SUEAIEditorWidget : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SUEAIEditorWidget)
    {}
    SLATE_END_ARGS()

    /** Construct this widget */
    void Construct(const FArguments& InArgs);

    /** Spawn the tab for this widget */
    static TSharedRef<SDockTab> SpawnTab(const FSpawnTabArgs& SpawnTabArgs);

private:
    /** Handle chat input submission */
    FReply OnChatSubmitted();

    /** Handle chat text commit */
    void OnChatTextCommitted(const FText& InText, ETextCommit::Type CommitType);

    /** Update chat history */
    void UpdateChatHistory(const FString& NewMessage);

    /** Clear chat history */
    FReply OnClearChatClicked();

    /** Send a test connection request */
    FReply OnTestConnectionClicked();

private:
    /** Chat input text box */
    TSharedPtr<SEditableTextBox> ChatInput;

    /** Chat history scroll box */
    TSharedPtr<SVerticalBox> ChatHistory;

    /** Connection status text */
    TSharedPtr<STextBlock> ConnectionStatus;

    /** Current session ID */
    FString SessionID;
};
