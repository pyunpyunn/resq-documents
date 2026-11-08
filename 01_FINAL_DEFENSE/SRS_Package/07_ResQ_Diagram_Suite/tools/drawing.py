"""Native SVG drawing and obstacle-aware orthogonal routing; no raster text."""
from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from PIL import ImageFont
import heapq
import math
import re

P = {
 'ink':'#0F1E3D','navy':'#12306B','blue':'#2563EB','cyan':'#0E7490','slate':'#475569',
 'navy-tint':'#E6ECF8','blue-tint':'#DBE8FE','cyan-tint':'#D5F0F6','slate-tint':'#E8EDF3',
 'mist':'#F5F8FD','white':'#FFFFFF','border':'#CBD5E1','border-strong':'#94A3B8','muted':'#64748B',
 'yes':'#166534','no':'#B91C1C',
}
COLOR={'web':'navy','household':'blue','rescuer':'cyan','shared':'slate','external':'slate'}
FONT=Path(__file__).resolve().parents[1]/'assets/Inter.ttf'
FONTS={}


def font(size=18,weight=600):
    key=size,weight
    if key not in FONTS:
        f=ImageFont.truetype(str(FONT if FONT.exists() else Path('C:/Windows/Fonts/segoeui.ttf')),size)
        if FONT.exists():
            try:f.set_variation_by_axes([14,weight])
            except (OSError,ValueError):pass
        FONTS[key]=f
    return FONTS[key]


def text_width(text,size=18,weight=600):return font(size,weight).getlength(str(text))


def wrap(text,width,size=18,weight=600):
    lines=[]
    for part in str(text).split('\n'):
        words=part.split();line=''
        for word in words:
            candidate=(line+' '+word).strip()
            if text_width(candidate,size,weight)<=width:line=candidate;continue
            if line:lines.append(line);line=''
            if text_width(word,size,weight)<=width:line=word;continue
            # Long schema identifiers wrap at underscores, never disappear.
            chunks=re.findall(r'[^_]+_?',word);piece=''
            for chunk in chunks:
                if piece and text_width(piece+chunk,size,weight)>width:lines.append(piece);piece=''
                piece+=chunk
            line=piece
        lines.append(line)
    return lines or ['']


def esc(s):return escape(str(s),quote=True)


@dataclass
class Node:
    key:str
    x:float
    y:float
    w:float
    h:float
    label:str
    kind:str='process'
    color:str='navy'
    fill:str='white'
    size:int=18
    data:dict=field(default_factory=dict)

    @property
    def right(self):return self.x+self.w
    @property
    def bottom(self):return self.y+self.h
    @property
    def cx(self):return self.x+self.w/2
    @property
    def cy(self):return self.y+self.h/2
    def port(self,side,offset=None):
        if side in ('w','e'):return (self.x if side=='w' else self.right,self.cy if offset is None else offset)
        return (self.cx if offset is None else offset,self.y if side=='n' else self.bottom)


@dataclass
class Edge:
    source:str
    target:str
    label:str=''
    color:str='navy'
    dashed:bool=False
    association:bool=False
    source_side:str|None=None
    target_side:str|None=None
    source_offset:float|None=None
    target_offset:float|None=None
    relation:dict|None=None
    via:list|None=None
    points:list=field(default_factory=list)


def compact(points):
    out=[]
    for p in points:
        p=tuple(round(v,2) for v in p)
        if out and p==out[-1]:continue
        if len(out)>1:
            a,b=out[-2:]
            if (a[0]==b[0]==p[0]) or (a[1]==b[1]==p[1]):out.pop()
        out.append(p)
    return out


class Router:
    def __init__(self,nodes):
        self.nodes=list(nodes.values());self.used={};self.cross={};self.failures=[]
        self.xs=sorted(x for x in {60, *[round(v,2) for n in self.nodes for v in (n.x-40,n.x-16,n.right+16,n.right+40)],max((n.right for n in self.nodes),default=600)+56} if x>=60)
        self.ys=sorted({116,*[round(v,2) for n in self.nodes for v in (n.y-40,n.y-16,n.bottom+16,n.bottom+40)],max((n.bottom for n in self.nodes),default=400)+56})
        self._clear={}

    def clear(self,a,b):
        a=tuple(a);b=tuple(b);key=(a,b) if a<b else (b,a)
        if key in self._clear:return self._clear[key]
        horizontal=abs(a[1]-b[1])<.01
        if not horizontal and abs(a[0]-b[0])>.01:return False
        lo,hi=sorted((a[0],b[0]) if horizontal else (a[1],b[1]));axis=a[1] if horizontal else a[0]
        for n in self.nodes:
            nlo,nhi=(n.y-3,n.bottom+3) if horizontal else (n.x-3,n.right+3)
            rlo,rhi=(n.x-3,n.right+3) if horizontal else (n.y-3,n.bottom+3)
            if nlo+.1<axis<nhi-.1 and max(lo,rlo)<min(hi,rhi)-.1:self._clear[key]=False;return False
        self._clear[key]=True;return True

    def cost(self,points):
        length=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(points,points[1:]))
        penalty=0
        for a,b in zip(points,points[1:]):
            horizontal=abs(a[1]-b[1])<.01;axis=round(a[1] if horizontal else a[0],2)
            lo,hi=sorted((a[0],b[0]) if horizontal else (a[1],b[1]))
            for qlo,qhi in self.used.get((horizontal,axis),[]):
                overlap=min(hi,qhi)-max(lo,qlo)
                if overlap>1:penalty+=overlap*5+120
        return length+22*max(0,len(points)-2)+penalty

    def remember(self,points):
        for a,b in zip(points,points[1:]):
            horizontal=abs(a[1]-b[1])<.01;axis=round(a[1] if horizontal else a[0],2)
            self.used.setdefault((horizontal,axis),[]).append(tuple(sorted((a[0],b[0]) if horizontal else (a[1],b[1]))))

    def route(self,a,b):
        a=tuple(round(v,2) for v in a);b=tuple(round(v,2) for v in b)
        candidates=[]
        if abs(a[0]-b[0])<.01 or abs(a[1]-b[1])<.01:candidates.append([a,b])
        candidates.extend([[a,(a[0],b[1]),b],[a,(b[0],a[1]),b]])
        for x in sorted(self.xs,key=lambda x:abs(x-a[0])+abs(x-b[0]))[:22]:candidates.append([a,(x,a[1]),(x,b[1]),b])
        for y in sorted(self.ys,key=lambda y:abs(y-a[1])+abs(y-b[1]))[:22]:candidates.append([a,(a[0],y),(b[0],y),b])
        valid=[compact(p) for p in candidates if all(self.clear(u,v) for u,v in zip(p,p[1:]))]
        if valid:
            answer=min(valid,key=self.cost)
            # A short, unobstructed candidate normally beats a global search.
            self.remember(answer);return answer
        xs=sorted(set(self.xs+[a[0],b[0]]));ys=sorted(set(self.ys+[a[1],b[1]]));xi={x:i for i,x in enumerate(xs)};yi={y:i for i,y in enumerate(ys)}
        start=(xi[a[0]],yi[a[1]],-1);goal=(xi[b[0]],yi[b[1]])
        heap=[(0,0,start)];dist={start:0};parent={};found=None
        while heap:
            _,cost,state=heapq.heappop(heap)
            if cost!=dist.get(state):continue
            x,y,direction=state
            if (x,y)==goal:found=state;break
            for nx,ny,nd in ((x-1,y,0),(x+1,y,0),(x,y-1,1),(x,y+1,1)):
                if not(0<=nx<len(xs) and 0<=ny<len(ys)):continue
                u=(xs[x],ys[y]);v=(xs[nx],ys[ny])
                if not self.clear(u,v):continue
                new=cost+self.cost([u,v])+(20 if direction not in (-1,nd) else 0)
                ns=(nx,ny,nd)
                if new<dist.get(ns,float('inf')):
                    dist[ns]=new;parent[ns]=state
                    heuristic=abs(xs[nx]-b[0])+abs(ys[ny]-b[1]);heapq.heappush(heap,(new+heuristic,new,ns))
            if len(dist)>250000:break
        if found is None:raise RuntimeError(f'No unobstructed orthogonal route from {a} to {b}')
        path=[];s=found
        while True:
            path.append((xs[s[0]],ys[s[1]]))
            if s==start:break
            s=parent[s]
        answer=compact(path[::-1]);self.remember(answer);return answer


class Diagram:
    def __init__(self,title,kind,scope):
        self.title=title;self.kind=kind;self.scope=scope
        self.groups={k:[] for k in ('Title','Containers','Connectors','Nodes','Labels')}
        self.nodes={};self.edges=[];self.bounds=[60,140,600,400];self.label_boxes=[];self.audit={'obstacle_routes':0,'label_obstructions':0}
        self.text(60,72,title,34,'navy',600,group='Title',max_width=1600)
        self.raw('<rect x="60" y="88" width="64" height="5" rx="2.5" fill="'+P['blue']+'"/>','Title')

    def raw(self,s,group='Nodes'):self.groups[group].append(s)

    def extent(self,x,y,w,h):
        self.bounds[0]=min(self.bounds[0],x);self.bounds[1]=min(self.bounds[1],y);self.bounds[2]=max(self.bounds[2],x+w);self.bounds[3]=max(self.bounds[3],y+h)

    def text(self,x,y,text,size=18,color='ink',weight=600,anchor='start',group='Nodes',max_width=None,line_height=None):
        lines=wrap(text,max_width,size,weight) if max_width else str(text).split('\n');lh=line_height or size+6
        for i,line in enumerate(lines):
            if not line:continue
            self.raw(f'<text x="{x:.2f}" y="{y+i*lh:.2f}" fill="{P.get(color,color)}" font-family="Inter, Segoe UI, Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(line)}</text>',group)
            w=text_width(line,size,weight);left=x-w/2 if anchor=='middle' else x-w if anchor=='end' else x
            self.extent(left,y+i*lh-size,w,lh)
        return len(lines)*lh

    def center_text(self,x,y,w,h,label,size=18,color='ink',weight=600,max_width=None,group='Nodes'):
        lines=wrap(label,max_width or w-24,size,weight);lh=size+6
        if size+(len(lines)-1)*lh>h-8:raise ValueError(f'Text does not fit node: {label} ({w}x{h})')
        top=y+h/2-(len(lines)-1)*lh/2+size*.34
        self.text(x+w/2,top,'\n'.join(lines),size,color,weight,'middle',group,line_height=lh)

    def container(self,x,y,w,h,label,color='slate',fill='mist',header=False):
        self.extent(x,y,w,h)
        self.raw(f'<g data-container="{esc(label)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{P[fill]}" stroke="{P[color]}" stroke-width="1.5"/></g>','Containers')
        if header:
            self.raw(f'<path d="M{x+16} {y}H{x+w-16}Q{x+w} {y} {x+w} {y+16}V{y+48}H{x}V{y+16}Q{x} {y} {x+16} {y}Z" fill="{P[color]}"/>','Containers')
            self.text(x+16,y+31,label.upper(),16,'white',600,group='Containers')
        else:self.text(x+16,y+27,label.upper(),14,color,600,group='Containers')

    def add(self,node,draw=True):
        if node.key in self.nodes:raise ValueError('Duplicate node '+node.key)
        self.nodes[node.key]=node;self.extent(node.x,node.y,node.w,node.h)
        if draw:self.draw_node(node)
        return node

    def draw_node(self,n):
        x,y,w,h=n.x,n.y,n.w,n.h;color=P[n.color];fill=P[n.fill]
        self.raw(f'<g id="{esc(n.key)}" data-node="{esc(n.key)}" data-label="{esc(n.label)}" data-kind="{n.kind}">')
        if n.kind in ('process','external','subprocess','split','primary'):
            if n.kind=='split':
                self.raw(f'<path d="M{x+10} {y}H{x+w/2}V{y+h}H{x+10}Q{x} {y+h} {x} {y+h-10}V{y+10}Q{x} {y} {x+10} {y}Z" fill="{P["blue"]}"/><path d="M{x+w/2} {y}H{x+w-10}Q{x+w} {y} {x+w} {y+10}V{y+h-10}Q{x+w} {y+h} {x+w-10} {y+h}H{x+w/2}Z" fill="{P["cyan"]}"/>')
            else:self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
            if n.kind=='subprocess':self.raw(f'<path d="M{x+10} {y}V{y+h}M{x+w-10} {y}V{y+h}" stroke="{color}" fill="none" stroke-width="1.5"/>')
        elif n.kind=='terminator':self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        elif n.kind=='decision':self.raw(f'<path d="M{x+w/2} {y}L{x+w} {y+h/2}L{x+w/2} {y+h}L{x} {y+h/2}Z" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        elif n.kind=='io':self.raw(f'<path d="M{x+20} {y}H{x+w}L{x+w-20} {y+h}H{x}Z" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        elif n.kind=='database':
            self.raw(f'<path d="M{x} {y+12}A{w/2} 12 0 0 1 {x+w} {y+12}V{y+h-12}A{w/2} 12 0 0 1 {x} {y+h-12}Z" fill="{fill}" stroke="{color}" stroke-width="1.5"/><path d="M{x} {y+12}A{w/2} 12 0 0 0 {x+w} {y+12}" fill="none" stroke="{color}" stroke-width="1.5"/>')
        elif n.kind=='usecase':self.raw(f'<ellipse cx="{n.cx}" cy="{n.cy}" rx="{w/2}" ry="{h/2}" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        elif n.kind=='dfd':
            self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{P["white"]}" stroke="{color}" stroke-width="1.75"/><path d="M{x+14} {y}H{x+w-14}Q{x+w} {y} {x+w} {y+14}V{y+36}H{x}V{y+14}Q{x} {y} {x+14} {y}Z" fill="{P["navy-tint"]}"/>')
            self.text(x+16,y+25,n.data['process_id'],16,'navy',600)
            self.center_text(x,y+36,w,h-36,n.label,n.size)
        elif n.kind=='store':
            self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{P["navy-tint"]}"/><path d="M{x+w} {y}H{x}V{y+h}H{x+w}" fill="none" stroke="{P["navy"]}" stroke-width="1.75"/><rect x="{x}" y="{y}" width="64" height="{h}" fill="{P["navy"]}" stroke="{P["navy"]}" stroke-width="1.75"/>')
            self.center_text(x,y,64,h,n.data['store_id'],18,'white',max_width=56)
            self.center_text(x+64,y,w-64,h,n.label,n.size)
        elif n.kind=='actor':
            cx=n.cx;self.raw(f'<circle cx="{cx}" cy="{y+10}" r="9" fill="{P["white"]}" stroke="{color}" stroke-width="1.75"/><path d="M{cx} {y+19}V{y+42}M{cx-20} {y+29}H{cx+20}M{cx} {y+42}L{cx-17} {y+65}M{cx} {y+42}L{cx+17} {y+65}" fill="none" stroke="{color}" stroke-width="1.75" stroke-linecap="round"/>')
            self.raw(f'<rect x="{x}" y="{y+74}" width="{w}" height="{h-74}" fill="{P["white"]}"/>')
            self.text(cx,y+88,n.label,18,n.color,600,'middle',max_width=w)
        else:raise ValueError(n.kind)
        if n.kind not in ('dfd','store','actor'):
            text_color='white' if n.kind=='split' or n.fill in ('navy','blue','cyan','slate') else 'ink'
            yy=y+6 if n.kind=='database' else y;hh=h-6 if n.kind=='database' else h
            self.center_text(x,yy,w,hh,n.label,n.size,text_color,max_width=w*(.62 if n.kind=='decision' else .78 if n.kind=='usecase' else .9))
        self.raw('</g>')

    def connect(self,source,target,**kwargs):
        if self.kind in ('03_Flow_Chart','04_Swim_Lane'):
            branch=kwargs.get('label','').lower()
            if branch in ('yes','no'):kwargs['color']=branch
        self.edges.append(Edge(source,target,**kwargs))

    def chip(self,x,y,label,color='slate',size=14):
        lines=wrap(label,220,size);w=max(text_width(line,size) for line in lines)+16;h=len(lines)*(size+4)+8
        x-=w/2;y-=h/2
        self.raw(f'<g data-connector-label="{esc(label)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{P["white"]}" stroke="{P["border"]}" stroke-width="1"/>','Labels')
        self.center_text(x,y,w,h,'\n'.join(lines),size,color,max_width=w-8,group='Labels');self.raw('</g>','Labels');self.extent(x,y,w,h);self.label_boxes.append((x,y,w,h))

    def _ports(self,e):
        a,b=self.nodes[e.source],self.nodes[e.target];dx=b.cx-a.cx;dy=b.cy-a.cy
        if e.source_side:ss=e.source_side
        elif abs(dx)>(a.w+b.w)/2:ss='e' if dx>0 else 'w'
        else:ss='s' if dy>0 else 'n'
        ts=e.target_side or {'e':'w','w':'e','s':'n','n':'s'}[ss]
        p=a.port(ss,e.source_offset)
        if e.association and a.kind=='actor':p=(a.cx+20,a.y+29)
        return p,b.port(ts,e.target_offset),ss,ts

    def draw_edges(self):
        # Control-flow branches leave visibly different faces. Other fan-outs
        # use distinct ports instead of one shared, ambiguous exit point.
        if self.kind=='03_Flow_Chart':
            for e in self.edges:
                source=self.nodes[e.source];target=self.nodes[e.target]
                if source.kind=='decision':
                    e.source_side='s' if e.label=='Yes' else 'w' if target.cx<source.cx else 'e'
                    e.target_side='n'
            ports={}
            for e in self.edges:
                source=self.nodes[e.source]
                if source.kind not in ('process','subprocess'):continue
                side=self._ports(e)[2];ports.setdefault((e.source,side),[]).append(e)
            for (key,side),edges in ports.items():
                if len(edges)<2:continue
                node=self.nodes[key]
                for i,e in enumerate(edges):
                    fraction=.2+.6*i/(len(edges)-1)
                    e.source_side=side;e.source_offset=node.y+node.h*fraction if side in ('w','e') else node.x+node.w*fraction
        router=Router(self.nodes);vectors={'e':(1,0),'w':(-1,0),'s':(0,1),'n':(0,-1)}
        for index,e in enumerate(self.edges):
            p,q,ss,ts=self._ports(e)
            if e.association:
                points=[p,q]
            elif e.via is not None:
                points=compact([p]+e.via+[q])
            else:
                vx,vy=vectors[ss];wx,wy=vectors[ts];a=(round(p[0]+vx*16,2),round(p[1]+vy*16,2));b=(round(q[0]+wx*16,2),round(q[1]+wy*16,2))
                points=compact([p]+router.route(a,b)+[q]);self.audit['obstacle_routes']+=1
            e.points=points
            d=' '.join(('M' if i==0 else 'L')+f'{x:.2f},{y:.2f}' for i,(x,y) in enumerate(points));dash=' stroke-dasharray="7 5"' if e.dashed else '';opacity='';weight=2.25 if self.kind=='02_Use_Case' or e.color in ('yes','no') else 1.75
            self.raw(f'<path data-edge="{index}" data-source="{esc(e.source)}" data-target="{esc(e.target)}" d="{d}" fill="none" stroke="{P[e.color]}" stroke-width="{weight}" stroke-linecap="round" stroke-linejoin="round"{dash}{opacity}/>','Connectors')
            for x,y in points:self.extent(x,y,0,0)
            if e.relation:self.cardinality(points,e.relation)
            elif not e.association:self.arrow(points[-2],points[-1],e.color)
            if e.label:
                lines=wrap(e.label,220,14);cw=max(text_width(line,14) for line in lines)+16;ch=len(lines)*18+8
                segments=sorted(zip(points,points[1:]),key=lambda s:abs(s[0][0]-s[1][0])+abs(s[0][1]-s[1][1]),reverse=True);choice=None
                for a,b in segments:
                    length=math.hypot(b[0]-a[0],b[1]-a[1])
                    fractions=[.5,.35,.65,.2,.8]+[distance/length for distance in range(16,int(length),24)] if length else [.5]
                    for fraction in fractions:
                        base_x=a[0]+(b[0]-a[0])*fraction;base_y=a[1]+(b[1]-a[1])*fraction
                        offsets=[(0,0)]
                        if self.kind=='05_Data_Flow':
                            offsets=[(0,-ch/2-10),(0,ch/2+10)] if abs(a[1]-b[1])<.01 else [(cw/2+10,0),(-cw/2-10,0)]
                        for ox,oy in offsets:
                            cx,cy=base_x+ox,base_y+oy
                            blocked=any(cx+cw/2>n.x-2 and cx-cw/2<n.right+2 and cy+ch/2>n.y-2 and cy-ch/2<n.bottom+2 for n in self.nodes.values())
                            blocked=blocked or any(cx+cw/2>x-2 and cx-cw/2<x+w+2 and cy+ch/2>y-2 and cy-ch/2<y+h+2 for x,y,w,h in self.label_boxes)
                            if self.kind=='05_Data_Flow':
                                for u,v in zip(points,points[1:]):
                                    if abs(u[1]-v[1])<.01:
                                        hit=cy-ch/2-2<u[1]<cy+ch/2+2 and max(min(u[0],v[0]),cx-cw/2-2)<min(max(u[0],v[0]),cx+cw/2+2)
                                    else:hit=cx-cw/2-2<u[0]<cx+cw/2+2 and max(min(u[1],v[1]),cy-ch/2-2)<min(max(u[1],v[1]),cy+ch/2+2)
                                    if hit:blocked=True;break
                            if not blocked:choice=(cx,cy);break
                        if choice:break
                    if choice:break
                if choice is None:
                    a,b=segments[0];choice=((a[0]+b[0])/2,(a[1]+b[1])/2);self.audit['label_obstructions']+=1
                    self.audit.setdefault('label_details',[]).append({'source':e.source,'target':e.target,'label':e.label,'points':points})
                self.chip(*choice,e.label,e.color)
                e.label_box=self.label_boxes[-1]

    def arrow(self,a,b,color='navy'):
        dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
        if not length:return
        ux,uy=dx/length,dy/length;vx,vy=-uy,ux
        pts=[b,(b[0]-10*ux+4.5*vx,b[1]-10*uy+4.5*vy),(b[0]-10*ux-4.5*vx,b[1]-10*uy-4.5*vy)]
        self.raw('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="{P[color]}"/>','Connectors')

    def cardinality(self,points,rel):
        for end,optional,many in ((0,rel['cardinality'].startswith('|o'),False),(-1,'o' in rel['cardinality'].split('--')[-1].split('..')[-1],rel['cardinality'].endswith('{'))):
            a=points[end];b=points[1] if end==0 else points[-2];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);ux,uy=dx/length,dy/length;vx,vy=-uy,ux
            if many:
                tip=(a[0]+14*ux,a[1]+14*uy)
                for offset in (-7,0,7):self.raw(f'<path d="M{tip[0]} {tip[1]}L{a[0]+offset*vx} {a[1]+offset*vy}" stroke="{P["navy"]}" stroke-width="1.75" fill="none"/>','Connectors')
            else:
                x,y=a[0]+8*ux,a[1]+8*uy;self.raw(f'<path d="M{x-6*vx} {y-6*vy}L{x+6*vx} {y+6*vy}" stroke="{P["navy"]}" stroke-width="1.75"/>','Connectors')
            if optional:self.raw(f'<circle cx="{a[0]+24*ux}" cy="{a[1]+24*uy}" r="4" fill="{P["white"]}" stroke="{P["navy"]}" stroke-width="1.75"/>','Connectors')

    def save(self,path):
        self.draw_edges()
        width=math.ceil(max(self.bounds[2]+60,text_width(self.title,34)+120)/8)*8;height=math.ceil((self.bounds[3]+60)/8)*8
        parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(self.title)}">',f'<rect width="{width}" height="{height}" fill="{P["white"]}"/>']
        # Named SVG groups and native text remain editable when imported into Figma.
        for name in ('Title','Containers','Connectors','Nodes','Labels'):parts.append(f'<g id="{name}">'+''.join(self.groups[name])+'</g>')
        parts.append('</svg>');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(parts),encoding='utf-8')
        return {'file':str(path),'width':width,'height':height,'title':self.title,'family':self.kind,'scope':self.scope,'nodes':len(self.nodes),'edges':len(self.edges),'audit':self.audit,'node_data':[{'key':n.key,'x':n.x,'y':n.y,'w':n.w,'h':n.h,'kind':n.kind,'label':n.label} for n in self.nodes.values()],'edge_data':[{'source':e.source,'target':e.target,'points':e.points,'association':e.association,'uml':getattr(e,'data_uml',False),'label':e.label,'color':e.color,'label_box':getattr(e,'label_box',None)} for e in self.edges]}
