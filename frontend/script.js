const API_BASE_URL = "http://localhost:8000"; // Replace with your FastAPI server URL

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const videoForm = document.getElementById("videoForm");
    const questionForm = document.getElementById("questionForm");
    const logoutButton = document.getElementById("logoutButton");

    // Function to decode JWT token and get user ID
    const getUserIdFromToken = () => {
        const token = localStorage.getItem("token");
        if (!token) return null;

        try {
            const payload = JSON.parse(atob(token.split('.')[1])); // Decode the token payload
            return payload.sub; // Return the user ID from the token
        } catch (error) {
            console.error("Failed to decode token:", error);
            return null;
        }
    };

    // Login Form
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("name").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch(`${API_BASE_URL}/login/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ name, password }),
                });

                if (!response.ok) {
                    throw new Error("Login failed");
                }

                const data = await response.json();
                localStorage.setItem("token", data.token); // Save the token to localStorage
                alert("Login successful!");
                window.location.href = "main.html"; // Redirect to the main page
            } catch (error) {
                alert("Login failed. Please check your credentials and try again.");
            }
        });
    }

    // Signup Form
    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const name = document.getElementById("name").value;
            const phone = document.getElementById("phone").value ;
            const password = document.getElementById("password").value;
            console.log("phone number",phone);
            if (!/^\d{10}$/.test(phone)) {
                alert("Phone number must be exactly 10 digits.");
                return; // Stop form submission
            }    

            try {
                const response = await fetch(`${API_BASE_URL}/users/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ name, phone, password }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Backend error:", errorData);
                    throw new Error("Signup failed");
                }

                alert("Signup successful. Please login.");
                window.location.href = "index.html"; // Redirect to the login page
            } catch (error) {
                alert("Signup failed. Please try again.");
            }
        });
    }

    // Video Form
    if (videoForm) {
        videoForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const audioFile = document.getElementById("audioFile").files[0];
            const token = localStorage.getItem("token");

            if (!token) {
                alert("Please login again.");
                window.location.href = "index.html";
                return;
            }

            if (!audioFile) {
                alert("Please select an audio file.");
                return;
            }

            const formData = new FormData();
            formData.append("audio_file", audioFile);

            try {
                const response = await fetch(`${API_BASE_URL}/videos/`, {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                    body: formData,
                });

                if (response.status === 401) {
                    localStorage.removeItem("token");
                    alert("Your session has expired. Please login again.");
                    window.location.href = "index.html";
                    return;
                }

                if (!response.ok) {
                    throw new Error("Failed to upload audio file");
                }

                const data = await response.json();
                alert(`Audio file uploaded successfully. Task ID: ${data.task_id}`);

                // Set the file_path in the hidden input field
                const filePathInput = document.getElementById("filePath");
                if (filePathInput) {
                    filePathInput.value = data.file_path; // Assuming the response contains the file_path
                }
            } catch (error) {
                alert("Failed to upload audio file. Please try again.");
            }
        });
    }

    // Question Form
    if (questionForm) {
        questionForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const questionInput = document.getElementById("question");
            const filePathInput = document.getElementById("filePath"); // Assuming you have a hidden input for file_path

            if (!questionInput || !filePathInput) {
                console.error("Question input or file path input not found in the DOM.");
                return;
            }

            const question = questionInput.value;
            const filePath = filePathInput.value; // Get the file path from the hidden input
            const token = localStorage.getItem("token");

            if (!token) {
                alert("Please login again.");
                window.location.href = "index.html";
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/ask/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                    body: JSON.stringify({ 
                        file_path: filePath, // Include file_path in the payload
                        question: question 
                    }),
                });

                if (response.status === 401) {
                    localStorage.removeItem("token");
                    alert("Your session has expired. Please login again.");
                    window.location.href = "index.html";
                    return;
                }

                if (!response.ok) {
                    throw new Error("Failed to ask question");
                }

                const data = await response.json();
                document.getElementById("response").innerText = `Answer: ${data.answer}`;
            } catch (error) {
                alert("Failed to ask question. Please try again.");
            }
        });
    }

    // Logout Button
    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            localStorage.removeItem("token");
            alert("You have been logged out.");
            window.location.href = "index.html";
        });
    }
});