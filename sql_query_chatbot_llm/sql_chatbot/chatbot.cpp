#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <pqxx/pqxx>
#include <curl/curl.h>
#include <nlohmann/json.hpp> // JSON library for parsing responses

using namespace std;
using json = nlohmann::json;

// Structure to hold table-column mappings
struct OsqueryTable {
    string table;
    vector<string> columns;
};

// Function to load osquery table metadata from a file
unordered_map<string, OsqueryTable> loadMetadata(const string& filename) {
    unordered_map<string, OsqueryTable> metadata;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Failed to open file: " << filename << endl;
        exit(EXIT_FAILURE);
    }

    string line;
    getline(file, line); // Skip header
    while (getline(file, line)) {
        stringstream ss(line);
        string table, column;
        getline(ss, table, ',');
        getline(ss, column, ',');

        metadata[table].table = table;
        metadata[table].columns.push_back(column);
    }

    file.close();
    return metadata;
}

// Callback function for CURL response
size_t write_callback(void* contents, size_t size, size_t nmemb, string* out) {
    size_t total_size = size * nmemb;
    out->append(static_cast<char*>(contents), total_size);
    return total_size;
}

string callOpenAI(const string& userInput, const unordered_map<string, OsqueryTable>& metadata) {
    const string api_key = "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";

    if (api_key.empty()) {
        cerr << "OpenAI API key is missing!" << endl;
        return "ERROR";
    }

    string url = "https://api.openai.com/v1/completions";
    string prompt = "Generate an SQL query based on the following metadata and user input:\n";

    // Add metadata to the prompt
    int maxMetadataEntries = 5;
    for (const auto& [table, data] : metadata) {
        if (maxMetadataEntries-- == 0) break;
        prompt += "Table: " + table + ", Columns: ";
        for (const auto& column : data.columns) {
            prompt += column + " ";
        }
        prompt += "\n";
    }

    // Sanitize the user input (replace newline characters with space)
    string sanitized_input = userInput;
    std::replace(sanitized_input.begin(), sanitized_input.end(), '\n', ' ');

    prompt += "User Input: " + sanitized_input + "\nSQL Query:";

    // Prepare CURL request
    CURL* curl = curl_easy_init();
    if (!curl) {
        cerr << "CURL initialization failed!" << endl;
        return "ERROR";
    }

    string response_data;
    struct curl_slist* headers = nullptr;
    headers = curl_slist_append(headers, ("Authorization: Bearer " + api_key).c_str());
    headers = curl_slist_append(headers, "Content-Type: application/json");

    // Create JSON data for the POST request
    json post_data = {
        {"model", "text-davinci-003"},
        {"prompt", "Tell me a joke"},
        {"max_tokens", 100}
    };

    // Print the request body to debug
    cout << "Request Body: " << post_data.dump(4) << endl;

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data.dump().c_str());

    // Set the write callback and data
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);

    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_data);

    // Perform the CURL request
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        cerr << "CURL request failed: " << curl_easy_strerror(res) << endl;
    }

    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);

    if (response_data.empty()) {
        cerr << "Received an empty response from OpenAI API." << endl;
        return "ERROR";
    }

    // Print the raw response for debugging
    cout << "Raw Response Data: " << response_data << endl;

    // Try to parse the response data as JSON
    try {
        // Parse the response JSON
        json response_json = json::parse(response_data);

        // Check if the 'choices' field is present and extract the SQL query
        if (response_json.contains("choices") && !response_json["choices"].empty()) {
            string sql_query = response_json["choices"][0]["text"];
            cout << "Generated SQL Query: " << sql_query << endl;
            return sql_query;
        } else {
            cerr << "Invalid response format or no SQL query found." << endl;
            return "ERROR";
        }
    } catch (const json::exception& e) {
        cerr << "JSON Parsing error: " << e.what() << endl;
        cerr << "Response Data: " << response_data << endl;  // Print the raw response for further analysis
        return "ERROR";
    }
}

// Function to execute SQL query on PostgreSQL
void executeQuery(const string& query) {
    try {
        pqxx::connection conn("dbname=" + string(getenv("fleet")) +
                              " user=" + string(getenv("vajra")) +
                              " password=" + string(getenv("admin")));
        if (conn.is_open()) {
            pqxx::work txn(conn);
            pqxx::result result = txn.exec(query);

            cout << "Query Result:\n";
            for (const auto& row : result) {
                for (const auto& field : row) {
                    cout << field.c_str() << "\t";
                }
                cout << endl;
            }
            txn.commit();
        } else {
            cerr << "Failed to connect to database." << endl;
        }
    } catch (const exception& e) {
        cerr << "Database error: " << e.what() << endl;
    }
}
string parseOpenAIResponse(const string& response) {
    try {
        // Check if the response is empty or malformed
        if (response.empty()) {
            cerr << "Received an empty response." << endl;
            return "ERROR";
        }

        // Parse the response
        auto jsonResponse = json::parse(response);
        
        // Make sure the expected fields exist
        if (jsonResponse.contains("choices") && jsonResponse["choices"].size() > 0) {
            return jsonResponse["choices"][0]["text"];
        } else {
            cerr << "Invalid or unexpected response format." << endl;
            return "ERROR";
        }
    } catch (const exception& e) {
        cerr << "Error parsing OpenAI response: " << e.what() << endl;
        return "ERROR";
    }
}
// Main chatbot function
void chatbot(const unordered_map<string, OsqueryTable>& metadata) {
    cout << "Welcome to AI-powered osquery chatbot! Type 'exit' to quit.\n";

    string userInput;
    while (true) {
        cout << "\nYou: ";
        getline(cin, userInput);

        if (userInput == "exit") {
            cout << "Goodbye!" << endl;
            break;
        }

        string aiResponse = callOpenAI(userInput, metadata);
        string query = parseOpenAIResponse(aiResponse);

        if (query.find("ERROR") == string::npos) {
            cout << "Generated SQL Query: " << query << endl;
            executeQuery(query);
        } else {
            cout << query << endl;
        }
    }
}

// Main function
int main() {
    const string metadataFile = "/home/devesh/VajraServer/sql_chatbot/table_schemas.csv";
    unordered_map<string, OsqueryTable> metadata = loadMetadata(metadataFile);

    chatbot(metadata);

    return 0;
}
