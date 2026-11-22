<?php

function get_user_by_email($email)
{
    // Dummy data stands in for a MySQL users table.
    $users = [
        ["id" => 1, "name" => "Vijay Kumar", "email" => "vijay@example.com"],
        ["id" => 2, "name" => "Asha Sharma", "email" => "asha@example.com"],
    ];

    foreach ($users as $user) {
        if ($user["email"] === $email) {
            return $user;
        }
    }

    return null;
}

// Simulated JSON response from the AI for: "Find the user with email vijay@example.com."
$aiResponse = json_encode([
    "name" => "get_user_by_email",
    "arguments" => [
        "email" => "vijay@example.com",
    ],
]);

$toolCall = json_decode($aiResponse, true);
$result = null;

// Our PHP application dispatches the requested tool and returns its result.
switch ($toolCall["name"] ?? "") {
    case "get_user_by_email":
        $email = $toolCall["arguments"]["email"] ?? "";
        $result = get_user_by_email($email);
        break;
}

echo json_encode(["result" => $result], JSON_PRETTY_PRINT) . PHP_EOL;

