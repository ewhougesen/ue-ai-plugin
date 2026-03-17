// Copyright Epic Games, Inc. All Rights Reserved.

#include "UEAIEditorWidget.h"
#include "UEAIService.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SWindow.h"
#include "Widgets/Layout/SScrollBox.h"
#include "Widgets/Layout/SVerticalBox.h"
#include "Widgets/Text/SRichTextBlock.h"
#include "EditorStyleSet.h"
#include "HAL/PlatformApplicationMisc.h"

#define LOCTEXT_NAMESPACE "SUEAIEditorWidget"

void SUEAIEditorWidget::Construct(const FArguments& InArgs)
{
    // Generate session ID
    SessionID = FGuid::NewGuid().ToString();

    ChildSlot
    [
        SNew(SVerticalBox)

        // Header section
        + SVerticalBox::Slot()
        .AutoHeight()
        .Padding(5)
        [
            SNew(SHorizontalBox)

            + SHorizontalBox::Slot()
            .AutoWidth()
            .VAlign(VAlign_Center)
            .Padding(0, 0, 10, 0)
            [
                SNew(STextBlock)
                .Text(FText::FromString("UE AI Plugin"))
                .Font(FEditorStyle::GetFontStyle("FontAwesome.14"))
                .ColorAndOpacity(FLinearColor::White)
            ]

            + SHorizontalBox::Slot()
            .FillWidth(1.0f)
            .VAlign(VAlign_Center)
            [
                SNew(STextBlock)
                .Text(this, &SUEAIEditorWidget::GetConnectionStatusText)
                .ColorAndOpacity(this, &SUEAIEditorWidget::GetConnectionStatusColor)
            ]

            + SHorizontalBox::Slot()
            .AutoWidth()
            [
                SNew(SButton)
                .Text(LOCTEXT("TestConnection", "Test Connection"))
                .OnClicked(this, &SUEAIEditorWidget::OnTestConnectionClicked)
            ]
        ]

        // Chat history section
        + SVerticalBox::Slot()
        .FillHeight(1.0f)
        .Padding(5)
        [
            SNew(SScrollBox)
            [
                SAssignNew(ChatHistory, SVerticalBox)
                + SVerticalBox::Slot()
                .Padding(5)
                [
                    SNew(STextBlock)
                    .Text(LOCTEXT("Welcome", "Welcome to UE AI Plugin! Enter your request below."))
                    .ColorAndOpacity(FLinearColor::White)
                ]
            ]
        ]

        // Input section
        + SVerticalBox::Slot()
        .AutoHeight()
        .Padding(5)
        [
            SHorizontalBox::Slot()
            .FillWidth(1.0f)
            [
                SNew(SEditableTextBox)
                .Text(this, &SUEAIEditorWidget::GetChatInputText)
                .HintText(LOCTEXT("ChatHint", "Ask AI to help with your project..."))
                .OnTextCommitted(this, &SUEAIEditorWidget::OnChatTextCommitted)
                .ClearKeyboardFocusOnCommit(false)
                .MinDesiredWidth(400)
            ]
        ]

        // Button section
        + SVerticalBox::Slot()
        .AutoHeight()
        .Padding(5)
        [
            SNew(SHorizontalBox)

            + SHorizontalBox::Slot()
            .AutoWidth()
            [
                SNew(SButton)
                .Text(LOCTEXT("Send", "Send"))
                .OnClicked(this, &SUEAIEditorWidget::OnChatSubmitted)
            ]

            + SHorizontalBox::Slot()
            .Padding(10, 0)
            .AutoWidth()
            [
                SNew(SButton)
                .Text(LOCTEXT("ClearChat", "Clear Chat"))
                .OnClicked(this, &SUEAIEditorWidget::OnClearChatClicked)
            ]
        ]
    ];
}

TSharedRef<SDockTab> SUEAIEditorWidget::SpawnTab(const FSpawnTabArgs& SpawnTabArgs)
{
    return SNew(SDockTab)
    .TabRole(ETabRole::PanelTab)
    .Label(LOCTEXT("UEAIPluginTabLabel", "UE AI Plugin"))
    [
        SNew(SBox)
        [
            SNew(SUEAIEditorWidget)
        ]
    ];
}

FText SUEAIEditorWidget::GetConnectionStatusText() const
{
    if (FUEAIService::Get().IsConnected())
    {
        return LOCTEXT("Connected", "● Connected to Backend");
    }
    return LOCTEXT("Disconnected", "● Not Connected");
}

FSlateColor SUEAIEditorWidget::GetConnectionStatusColor() const
{
    if (FUEAIService::Get().IsConnected())
    {
        return FLinearColor(0.0f, 1.0f, 0.0f); // Green
    }
    return FLinearColor(1.0f, 0.0f, 0.0f); // Red
}

FText SUEAIEditorWidget::GetChatInputText() const
{
    return ChatInput.IsValid() ? ChatInput->GetText() : FText::GetEmpty();
}

FReply SUEAIEditorWidget::OnChatSubmitted()
{
    if (!ChatInput.IsValid())
    {
        return FReply::Handled();
    }

    FString UserMessage = ChatInput->GetText().ToString();
    if (UserMessage.IsEmpty())
    {
        return FReply::Handled();
    }

    // Add user message to chat
    UpdateChatHistory(FString::Printf(TEXT("You: %s"), *UserMessage));

    // Create AI request
    FUEAIRequest Request;
    Request.UserInput = UserMessage;
    Request.SessionID = SessionID;

    // Send request to AI service
    FUEAIService::Get().SendChatRequest(Request,
        [this](const FUEAIResponse& Response)
        {
            if (Response.bSuccess)
            {
                UpdateChatHistory(FString::Printf(TEXT("AI: %s"), *Response.Content));
            }
            else
            {
                UpdateChatHistory(FString::Printf(TEXT("Error: %s"), *Response.ErrorMessage));
            }
        }
    );

    // Clear input
    ChatInput->SetText(FText::GetEmpty());

    return FReply::Handled();
}

void SUEAIEditorWidget::OnChatTextCommitted(const FText& InText, ETextCommit::Type CommitType)
{
    if (CommitType == ETextCommit::OnEnter)
    {
        OnChatSubmitted();
    }
}

void SUEAIEditorWidget::UpdateChatHistory(const FString& NewMessage)
{
    if (!ChatHistory.IsValid())
    {
        return;
    }

    ChatHistory->AddSlot()
        .Padding(5)
        [
            SNew(STextBlock)
            .Text(FText::FromString(NewMessage))
            .ColorAndOpacity(FLinearColor::White)
            .WrapTextAt(600)
        ];
}

FReply SUEAIEditorWidget::OnClearChatClicked()
{
    if (ChatHistory.IsValid())
    {
        ChatHistory->ClearChildren();
        ChatHistory->AddSlot()
            .Padding(5)
            [
                SNew(STextBlock)
                .Text(LOCTEXT("ChatCleared", "Chat cleared."))
                .ColorAndOpacity(FLinearColor::Gray)
            ];
    }
    return FReply::Handled();
}

FReply SUEAIEditorWidget::OnTestConnectionClicked()
{
    // Send a test health check request
    FUEAIRequest Request;
    Request.UserInput = TEXT("ping");
    Request.SessionID = TEXT("health_check");

    FUEAIService::Get().SendChatRequest(Request,
        [this](const FUEAIResponse& Response)
        {
            if (Response.bSuccess)
            {
                UpdateChatHistory(TEXT("Connection test successful!"));
            }
            else
            {
                UpdateChatHistory(FString::Printf(TEXT("Connection test failed: %s"), *Response.ErrorMessage));
            }
        }
    );

    return FReply::Handled();
}

#undef LOCTEXT_NAMESPACE
