import { Component, OnInit } from '@angular/core';
import { ApiService, Artist } from '../api.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-collection',
  templateUrl: './collection.component.html',
  styleUrls: ['./collection.component.scss']
})
export class CollectionComponent implements OnInit {
  
  constructor(private api: ApiService) { }

  artists$: Observable<Artist[]>

  ngOnInit() {
    this.artists$ = this.api.getArtists();
  }

}
