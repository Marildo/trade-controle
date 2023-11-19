package com.example.tdc;

import com.google.gson.annotations.SerializedName;

public class Carteira {

    private String nome;
    private Double resultado;


    @SerializedName("saldo_ativos")
    private  Double saldoAtivos;

    @SerializedName("saldo_caixa")
    private  Double saldoCaixa;

    public Carteira() {
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public Double getResultado() {
        return resultado;
    }

    public void setResultado(Double resultado) {
        this.resultado = resultado;
    }

    public Double getSaldoAtivos() {
        return saldoAtivos;
    }

    public void setSaldoAtivos(Double saldoAtivos) {
        this.saldoAtivos = saldoAtivos;
    }

    public Double getSaldoCaixa() {
        return saldoCaixa;
    }

    public void setSaldoCaixa(Double saldoCaixa) {
        this.saldoCaixa = saldoCaixa;
    }
}
