package com.glitchdream.payload;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.InputStream;
import java.io.IOException;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Cria um WebView
        WebView webView = new WebView(this);
        setContentView(webView);

        // Configurações para permitir JavaScript
        webView.getSettings().setJavaScriptEnabled(true);

        // Carrega o payload JavaScript do assets
        String jsPayload = loadAsset("payload.js");

        // Define um WebViewClient para carregar uma página vazia e injetar o payload
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                // Injeta o payload JavaScript após a página vazia carregar
                view.evaluateJavascript(jsPayload, null);
            }
        });

        // Carrega uma página vazia para ter um contexto de WebView
        webView.loadUrl("about:blank");
    }

    // Função auxiliar para ler o arquivo do assets
    private String loadAsset(String filename) {
        String content = "";
        try {
            InputStream is = getAssets().open(filename);
            int size = is.available();
            byte[] buffer = new byte[size];
            is.read(buffer);
            is.close();
            content = new String(buffer, "UTF-8");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        return content;
    }
}
