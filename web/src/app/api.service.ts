import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Artist {
  id: number;
  name: string;
}

export interface Album {
  id: number;
  name: number;
  year?: number;
}

export interface Song {
  id: number;
  track: number;
  name: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  getArtists(): Observable<Artist[]> {
    return this.http.get<Artist[]>('http://localhost/api/artists');
  }

  getAlbums(artistId: number): Observable<Album[]> {
    return this.http.get<Album[]>(`http://localhost/api/artists/${artistId}/albums`);
  }

  getSongs(albumId: number): Observable<Song[]> {
    return this.http.get<Song[]>(`http://localhost/api/albums/${albumId}/songs`);
  }
}
