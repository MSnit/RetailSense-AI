def main():

    while True:

        print("\n========== RetailSense AI ==========")
        print("1. Register Customer")
        print("2. Customer Recognition")
        print("3. Product Detection")
        print("4. Sentiment Analysis")
        print("5. Retail Chatbot")
        print("6. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            from customer_module.register_customer import register_customer
            register_customer()

        elif choice == "2":
              from recognition_module.live_recognition import run_live_recognition
              run_live_recognition()
              
        elif choice == "3":
            from product_module.product_detection import run_product_detection
            run_product_detection()

        elif choice == "4":
            from sentiment_module.sentiment import run_sentiment_analysis
            run_sentiment_analysis()

        elif choice == "5":
            from chatbot_module.chatbot import run_chatbot
            run_chatbot()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()