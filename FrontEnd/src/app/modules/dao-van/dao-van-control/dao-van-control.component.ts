import { Component, OnInit } from '@angular/core';
import {FileService} from '../../../shell/shell-routing-service'
import{UserService} from '../../../login/user-authenticate-service'
import { NzThMeasureDirective } from 'ng-zorro-antd';
import { ActivatedRoute, Router } from '@angular/router';
//import {DaovanServiceService} from '../daovan-service.service'
@Component({
  selector: 'app-dao-van-control',
  templateUrl: './dao-van-control.component.html',
  styleUrls: ['./dao-van-control.component.scss'],
 // providers:[DaovanServiceService],
})
export class DaoVanControlComponent implements OnInit {
  
  constructor(private fileSrevice:FileService,
    private userService:UserService,
    private router:Router,
    
    ) {
      // if (this.router.getCurrentNavigation().extras.state != undefined) {
      //   console.log(this.router.getCurrentNavigation());
      //   if (this.router.getCurrentNavigation().extras.state.active.validCode != null) {
      //     this.validCode = this.router.getCurrentNavigation().extras.state.active.validCode;
      //     this.userinfo = this.router.getCurrentNavigation().extras.state.active.data;
      //   } else this.validCode = null;
      //   console.log(this.validCode);
      //   this.loading = true;
      // } else {
      //   console.log(this.router.getCurrentNavigation().extras.state != undefined);
      //   this.router.navigate(['login'], { replaceUrl: true });
      // }
    }
  
  ngOnInit() {
   
    
    //this.fileSrevice
  }
}
