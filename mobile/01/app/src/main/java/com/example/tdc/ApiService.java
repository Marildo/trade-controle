package com.example.tdc;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.PUT;

public interface ApiService {

    @GET("carteiras")
    Call<ResponseData> getCarteiras();

    @PUT("/notas/arquivos/search")
    Call<EmptyResponse> searchNotas();
}
