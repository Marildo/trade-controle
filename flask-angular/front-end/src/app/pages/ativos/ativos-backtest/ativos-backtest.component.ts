import { Component, OnInit } from '@angular/core';
import { AtivoService } from '../../../service/api/ativo.service';
import { FormControl, FormGroup } from '@angular/forms';
import { ModalService } from 'src/app/components/modal/modal-service';

@Component({
  selector: 'app-ativos-backtest',
  templateUrl: './ativos-backtest.component.html',
  styleUrls: ['./ativos-backtest.component.scss']
})
export class AtivosBacktestComponent implements OnInit {


  public formBacktest: FormGroup;
  public items: any[];
  public ativos: any[];
  public ativos_choice:any[];
  public selected: any;
  //private codigos = 'ENEV3, IGTI3, TASA4, STBP3, KEPL3, ALOS3, HAPV3, PRIO3, MBLY3, TECN3, JHSF3, TIMS3, RAIL3, EQTL3, AURE3, MEAL3, SOMA3, GGPS3, INTB3, CSMG3, NEOE3, CMIG3, HBSA3, TRIS3, VIVA3, TTEN3, ELET6, HYPE3, OPCT3, TRAD3, MRFG3, CURY3, RADL3, KLBN4, BMGB4, VIVT3, PGMN3, SRNA3, RENT3, RDOR3, GMAT3, BPAN4, ASAI3, NTCO3, LAVV3, CPLE3, NGRD3, CLSA3, LREN3, ALPA4, ODPV3, RANI3, FESA4, WEGE3, VBBR3, EVEN3, ZAMP3, SIMH3, EGIE3, CCRO3, VAMO3, UGPA3, MULT3, SMFT3, WIZC3, CMIG4, CRFB3, POMO4, SMTO3, FLRY3, LJQQ3, AMBP3, GRND3'
  private codigos = [];//'ENEV3; PRIO3; JHSF3; TIMS3; EQTL3';

  constructor(private service: AtivoService, private modalService: ModalService) {
    this.items = [];
    this.ativos = [];
    this.ativos_choice = [];
    this.selected = {};



    this.formBacktest = new FormGroup({
      ativos: new FormControl(this.codigos),
      start_date: new FormControl(new Date('2018-01-01').toISOString().split('T')[0]),
      end_date: new FormControl(new Date().toISOString().split('T')[0]),
      var_percent: new FormControl(2.5),
      stop: new FormControl(4),
      capital: new FormControl(1000.00),
      costs: new FormControl(1.5),
      expect_mat: new FormControl(0.1),
      volume_min: new FormControl(1500000)
    });
  }

  ngOnInit(): void {
    this.formBacktest.value.ativos = 'ENEV3; PRIO3; JHSF3; TIMS3; EQTL3'
    this.onRun()

    this.service.loadAll().subscribe({
      next: (resp) => {
       this.ativos_choice = resp.data.map((i: any) => i.codigo);  
       this.ativos_choice.sort()
      }        
    })
  }



  onRun() {
    this.service.runBacktest(this.formBacktest.value)
      .subscribe({
        next: (resp) => {
          this.items = resp.data.items
          this.ativos = resp.data.ativos
        },
        error: (e) => {
          console.error(e)
        }
      })
  }

  onRunToCSV() {
    const body = this.formBacktest.value
    this.service.runBacktestToCsv(body)
      .subscribe({
        next: (resp) => {
          const url = window.URL.createObjectURL(resp);
          const a = document.createElement('a');
          a.setAttribute('style', 'display: none');
          a.href = url;
          a.download =  `backtest_varPercent${body.var_percent}_stop${body.stop}_${body.start_date}_${body.end_date}.csv`
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        },
        error: (e) => {
          console.error(e)
        }
      })
  }

  onViewTrades(ativo: string) {
    this.modalService.open('modalTrades')

    const data = this.items.filter(i => i.ativo === ativo)
    this.selected = data[0]

  }

  onCloseTrade() {
    this.modalService.close('modalTrades')
  }
}

