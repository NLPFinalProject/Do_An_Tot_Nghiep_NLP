import { Component, OnInit, Input } from '@angular/core';
import { MessageService } from '@app/core/services/Utils/message.service';
//import {DaovanServiceService} from '../../daovan-service.service'
@Component({
  selector: 'app-section-diff',
  templateUrl: './section-diff.component.html',
  styleUrls: ['./section-diff.component.scss'],
})
export class SectionDiffComponent implements OnInit {
  @Input() sessionData: any[];
  listOfSearchName: any = [];
  searchAddress: string;
  displayData: Array<object> = [];
  loading = true;
  data = [{}];
  fileList: Array<object> = [];
  constructor(private messageService: MessageService) {}
  ngOnInit(): void {
    this.getData();
  }
  ngOnChanges() {
    //this.childFunction()

    this.getData();
  }
  getData(): void {
    const number = Math.floor(Math.random() * 100);
    setTimeout(() => {
      this.displayData = [...this.sessionData];
      this.loading = false;
    }, number);
  }
}
