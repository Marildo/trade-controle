package com.example.tdc;

import java.util.List;

public class ResponseData {
  private List<Carteira> data;
  private boolean success;

    public ResponseData() {
    }

    public List<Carteira> getData() {
        return data;
    }

    public void setData(List<Carteira> data) {
        this.data = data;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }
}
