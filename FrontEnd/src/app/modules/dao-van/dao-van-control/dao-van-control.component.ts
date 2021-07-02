import { Component, OnInit } from '@angular/core';
import { FileService } from '../../../shell/shell-routing-service';

//import {DaovanServiceService} from '../daovan-service.service'
@Component({
  selector: 'app-dao-van-control',
  templateUrl: './dao-van-control.component.html',
  styleUrls: ['./dao-van-control.component.scss'],
  // providers:[DaovanServiceService],
})
export class DaoVanControlComponent implements OnInit {
  constructor(private fileSrevice: FileService) {}

  ngOnInit() {}
}
