console.log("CyberShield loaded successfully!");


function askBot() {

    const input = document.getElementById("user-question");
    const chatBox = document.getElementById("chat-box");

    if (!input || !chatBox) {
        return;
    }

    const question = input.value.trim();

    if (question === "") {
        alert("Please enter your question.");
        return;
    }


    // User message
    const userMessage = document.createElement("div");

    userMessage.className = "help-point";

    userMessage.innerHTML =
        "👤 <strong>You:</strong> " + question;

    chatBox.appendChild(userMessage);


    // Basic chatbot response
    let answer =
        "For your safety, do not share OTP, PIN, password or banking details with anyone.";


    const lowerQuestion = question.toLowerCase();


    if (lowerQuestion.includes("otp")) {

        answer =
            "🔐 Never share your OTP with anyone, even if they claim to be from your bank.";

    }
    else if (lowerQuestion.includes("upi")) {

        answer =
            "💳 Never enter your UPI PIN to receive money. Verify every payment request.";

    }
    else if (lowerQuestion.includes("phishing")) {

        answer =
            "🎣 Phishing messages often contain fake links. Check the website address before entering your details.";

    }
    else if (
        lowerQuestion.includes("password") ||
        lowerQuestion.includes("पासवर्ड")
    ) {

        answer =
            "🔑 Use a strong, unique password for every important account and enable 2-factor authentication.";

    }
    else if (
        lowerQuestion.includes("fraud") ||
        lowerQuestion.includes("scam")
    ) {

        answer =
            "🚨 If you face financial cyber fraud, contact your bank immediately and report it through the official cybercrime channels.";

    }


    // Bot response
    const botMessage = document.createElement("div");

    botMessage.className = "help-point";

    botMessage.innerHTML =
        "🤖 <strong>CyberShield:</strong> " + answer;

    chatBox.appendChild(botMessage);


    // Clear input
    input.value = "";

}