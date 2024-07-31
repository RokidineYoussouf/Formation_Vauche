<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centering List Items</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 20;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center; /* Center content horizontally */
            justify-content: center; /* Center content vertically */
            min-height: 100vh; /* Ensure the body takes full height */
        }
        .content {
            text-align: center; /* Center text inside the container */
        }
        ul {
            list-style: none; /* Remove default list styling */
            padding: 0;
        }
        li {
            margin-bottom: 10px; /* Space between list items */
        }
        p {
            margin: 0;
            text-align: justify; /* Justify text inside paragraphs */
            font-size: 1.2em; /* Adjust font size */
        }
        a {
            color: #028FD0;
            text-decoration: none;
            font-size: 3.2em; /* Adjust font size */
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="content">
        <ul>
            <li>
                <p align="justify">
                    <a href="https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/">Introducing Gemini 1.5, Google's next-generation AI model</a>.
                </p>
            </li>
                        <li>
                          </p>
                          ...
                            </p>
                             <li>
            
            <li>
                <p align="justify">
                    <a href="https://deepmind.google/technologies/gemini/">Gemini models Nouvelle Version</a>.
                </p>
            </li>
        </ul>
    </div>
</body>
</html>
