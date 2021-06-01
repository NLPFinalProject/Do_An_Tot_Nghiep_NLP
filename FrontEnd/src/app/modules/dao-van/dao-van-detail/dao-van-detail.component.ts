import { Component, OnInit } from '@angular/core';
import {DaovanServiceService} from '../daovan-service.service'

import { CommonModule } from '@angular/common';

import { SharedModule } from '@app/shared/shared.module';
//import { stringify } from '@angular/core/src/util';

import { TranslateModule } from '@ngx-translate/core';
import { ActivatedRoute, Router } from '@angular/router';
import { identity } from 'lodash';
//import throttleByAnimationFrame from 'ng-zorro-antd/core/util/throttleByAnimationFrame';
import { FileService } from '@../../../src/app/shell/shell-routing-service';
@Component({
  selector: 'app-dao-van-detail',
  templateUrl: './dao-van-detail.component.html',
  styleUrls: ['./dao-van-detail.component.scss'],
  providers:[DaovanServiceService]
})
export class DaoVanDetailComponent implements OnInit {
  public params:any;
  
 
 
  public currentId: number;
  public StoreNumber: number;
  public characterList1: any[];
  public characterList2: any[];
  public listchar: any[];
 
  public answer: any;
  public option: any[];
  public SelectedOption: number;
  public hitrate: any[];
  public trolling: boolean;
  ListHitRate: any[];
  public file1Name: any;
  public ratio: any[];
  HighestHitRate: any;
  
  public data:Array<any>=[
    {
      name:'yuragi sou',
      id:1,
      genre:'ecchi',
      ratio:10
    },
    {
      name:'to love ru',
      id:2,
      genre:'ecchi',
      ratio:20,
    },
    {
      name:'nisekoi',
      id:3,
      genre:'ecchi',
      ratio:30,
    },
    {
      name:'gotoubun',
      id:4,
      genre:'ecchi',
      ratio:25
    }
  ];
  public File1Name= this.data;
  public FileList2= this.data;
  
  constructor(
    
    private router: Router,
    private route: ActivatedRoute,
    private fileService: FileService,
    private activatedRoute: ActivatedRoute //private matDialog: MatDialog
  ) {
    // this.activatedRoute.queryParams.subscribe((params) => {
    //   console.log('new file');
    //   console.log(params);
    //   this.params = params;
    //   if (params.filename1 == undefined) {
    //     console.log('false');
    //     console.log(this.router.getCurrentNavigation());
    //     if (this.router.getCurrentNavigation().extras.state != null) {
    //       this.data = this.router.getCurrentNavigation().extras.state.data;
    //       console.log(this.data);
    //     }
        
    //   }
    //   // Print the parameter to the console.
    // });
  }
  


  ngOnInit() {
    //this.forgodTest();

    // this.characterList1 = [];
    // this.SelectedOption = 0;
    // this.ListHitRate = [];
    // this.ratio = null;
    // this.StoreNumber = 0;
    // this.currentId = -1;
    // this.answer = {
    //   ls1: null,
    //   ls2: null,
    //   ls3: null,
    // };

    // if (this.params.filename1 != undefined) {
    //   console.log(this.params.filename1);
    //   console.log('true');
    //   let temp = [];
    //   temp.push(this.params.listfile);
    //   let data = {
    //     id: this.params.id,
    //     filename1: this.params.filename1,
    //     listfile: temp,
    //     choice: 1,
    //   };
    //   console.log('data is');
    //   console.log(data);
    //   this.fileService.checkPlagiasm(data).subscribe(
    //     (data: any) => {
    //       this.data = data;
    //       this.trolling = false;

    //       // this.getFirstSentences();

    //       // this.ShowResult(0);
    //       // this.createOptionList();
    //     },
    //     (error) => {}
    //   );
    //  }
    
  }
}
