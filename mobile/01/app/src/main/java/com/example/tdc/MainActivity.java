package com.example.tdc;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import java.io.IOException;
import java.util.List;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.HttpException;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private TextView tv_loading;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tv_loading = findViewById(R.id.tv_loading);
        this.loadCarteiras();
        this.searchNotas();
    }

    public void recarregarCarteiras(View view) {

        this.loadCarteirasWIthRaw();
        this.tv_loading.setText("Carteiras carregadas com sucesso!");
    }

    private void loadCarteirasWIthRaw() {
        Request.Builder reqBuilder = new Request.Builder().get();
        reqBuilder.url("http://192.168.1.2/api/carteiras/");
        reqBuilder.addHeader("Accept", "application/json; charset=utf-8");
        reqBuilder.addHeader("Content-Type", "application/json");

        Request request = reqBuilder.build();


        OkHttpClient client = new OkHttpClient();

        client.newCall(request).enqueue(new okhttp3.Callback() {
            @Override
            public void onFailure(okhttp3.Call call, IOException e) {

            }

            @Override
            public void onResponse(okhttp3.Call call, okhttp3.Response response) throws IOException {
                var body =response.body();
                System.out.println(body.string());
            }
        });

    }

    public void loadCarteiras() {
        ApiService apiService = ApiClient.getApiService();


        Call<ResponseData> call = apiService.getCarteiras();
        call.enqueue(new Callback<ResponseData>() {


            @Override
            public void onResponse(Call<ResponseData> call, Response<ResponseData> response) {

                Double saldo_caixa = 0.0;
                Double saldo_ativos = 0.0;
                Double resultado = 0.0;
                List<Carteira> carteiras = response.body().getData();
                for (Carteira carteira : carteiras) {
                    saldo_caixa += carteira.getSaldoCaixa();
                    saldo_ativos += carteira.getSaldoAtivos();
                    resultado += carteira.getResultado();
                }

                TextView tv_saldo_caixa = findViewById(R.id.tv_saldo_caixa);
                tv_saldo_caixa.setText(saldo_caixa.toString());

                TextView tv_saldo_ativos = findViewById(R.id.tv_saldo_ativo);
                tv_saldo_ativos.setText(saldo_ativos.toString());

                TextView tv_patrimonio = findViewById(R.id.tv_patrimonio);
                Double patrimonio = saldo_ativos + saldo_caixa;
                tv_patrimonio.setText(patrimonio.toString());

                TextView tv_resultado = findViewById(R.id.tv_resultado);
                tv_resultado.setText(resultado.toString());
            }

            @Override
            public void onFailure(Call<ResponseData> call, Throwable t) {
                ResponseBody errorBody = ((HttpException) t).response().errorBody();
                try {
                    String body = errorBody.string();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }

                tv_loading.setText("Response not successful. Code: " + t.getMessage());
                t.printStackTrace();
            }
        });
    }

    public void searchNotas() {
        tv_loading.setText("Procurando por notas");
        ApiService apiService = ApiClient.getApiService();
        Call<EmptyResponse> call = apiService.searchNotas();
        call.enqueue(new Callback<EmptyResponse>() {
            @Override
            public void onResponse(Call<EmptyResponse> call, Response<EmptyResponse> response) {
                if (response.code() == 200) {
                    tv_loading.setText("Notas carregadas com sucesso");
                    loadCarteiras();
                }
            }

            @Override
            public void onFailure(Call<EmptyResponse> call, Throwable t) {
                tv_loading.setText("Falha ai carregar notas. " + t.getMessage());
                t.printStackTrace();
            }
        });
    }
}