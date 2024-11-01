//
//  ContentView.swift
//  daypack
//
//  Created by Joe Bowser on 2024-10-16.
//

import SwiftUI
import WebKit

struct ContentView: View {
    @State private var webviewUrl: String
    
    init() {
        // Load URL from config.json at initialization
        self.webviewUrl = Self.loadConfiguration() ?? "http://localhost:3000"
    }
    
    private static func loadConfiguration() -> String? {
        guard let configPath = Bundle.main.path(forResource: "config", ofType: "json"),
              let configData = try? Data(contentsOf: URL(fileURLWithPath: configPath)),
              let config = try? JSONDecoder().decode(Config.self, from: configData) else {
            return nil
        }
        return config.webviewUrl
    }
    
    var body: some View {
        WebView(url: URL(string: webviewUrl)!)
    }
}

struct Config: Codable {
    let webviewUrl: String
}

#Preview {
    ContentView()
}

struct WebView: UIViewRepresentable {
    let url: URL
    
    func makeUIView(context: Context) -> WKWebView {
        return WKWebView()
    }
    
    func updateUIView(_ webView: WKWebView, context: Context) {
        let request = URLRequest(url: url)
        webView.load(request)
    }
}
