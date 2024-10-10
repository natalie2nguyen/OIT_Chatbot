// chatApi.ts

export const sendMessageToChatbot = async (message: string): Promise<string> => {
    const data = { message };
  
    try {
        // Attempt to make a POST request to the chatbot server
        const res = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        });

        // If the response is not OK, throw an error
        if (!res.ok) {
        throw new Error('HTTP Error! Status: ' + res.status);
        }

        // Return the response as JSON
        const json: { response: string } = await res.json();
        return json.response;
    } catch (error) {
        console.error('Error:', error);
        return 'An error occurred while processing your request.';
    }
  };
  