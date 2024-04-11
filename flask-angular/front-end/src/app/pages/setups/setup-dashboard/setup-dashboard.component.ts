import { Component, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { Subscription, interval, timeout } from 'rxjs';
 

 

import { SetupService } from 'src/app/service/api/setup.service';

@Component({
  selector: 'app-setup-dashboard',
  templateUrl: './setup-dashboard.component.html',
  styleUrls: ['./setup-dashboard.component.scss']
})
export class SetupDashboardComponent implements OnInit {

  public indiceData?: any;
  public update_at?: Date;
  private timerSubscription: Subscription | undefined;

 

  constructor(
    private setupService: SetupService,
    private messageService: MessageService) {

  }
  ngOnInit(): void {
    this.load()
    this.startTimer();
  }


  load() {
    this.setupService.indiceFut().subscribe({
      next: (resp) => {
        this.indiceData = resp.data
        this.update_at = new Date()
         
      },
      error(err) {
        console.error(err)
        // this.messageService.add({ severity: 'error', summary: 'Erro', detail: err.data, life: 5000 })
      },
    })
  }

 

   


  private startTimer(): void {
    const timerObservable = interval(1 * 60 * 1000); // 5 minutos em milissegundos

    this.timerSubscription = timerObservable
      .subscribe(() => {
        this.load();
      });
  }


}
