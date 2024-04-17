sonic_pi_algo = """

#####################################################################################################

#PARÀMETRES PRINCIPALS#

#variable que ho randomitza tot# USUARI
cançonsInfinites = {}
#LA LLAVOR DE RANDOMITZACIÓ AGAFA EL VALOR DE "cançonsInfinites"
use_random_seed cançonsInfinites

########complexitat del beat# 0-8, integers# USUARI
cb = [0,0,0,1,1,1,2,2.5,3,3,4,4,5,6,7,8][rrand_i(0,12)]

########complexitat del sample# 1-4, integers# USUARI 
cs = 4

########chop de A
desplasamp = rrand_i(0,50)
salts = 1
desplasampC = rrand_i(0,50)
saltsampgreuC = 1
########chop de B
desplasampB = rrand_i(0,50)
saltsB = 1
desplasampBC = rrand_i(0,50)
saltsampgreuBC = 1

########Control delays# USUARI 
modifdelaysampagut = 0.10
modifdelaysampgreu = 0.05
controldelaybeat = 0.00

########sonsbatera# USUARI
canvisonsbatera = 1

########afinació# USUARI
afinat = 0

########tempo#USUARI
use_bpm rrand_i(85,95)

########ESTRUCTURA# USUARI(NOMÉS m I w)
m=2
#m=quantes vegades sona la A 
w=1
#w=quantes vegades sona la B
y=3
z=1
#y i z determinen l'estructura d'un patró 4x4 (o de dos, si factoramplitud==2)
u=4
#u determina quantes negres té cada compàs de sample

#####################################################################################################

#RUTES ARXIUS#

base_dir = "/audio"
sn = base_dir + "/AB Snares, Snaps, Claps"
bd = base_dir + "/AB Kicks"
hh = base_dir + "/AB Hats"
starters = base_dir + "/Samples - startersDEF" if cs==3 || cs==4
starters = base_dir + "/Samples - starters" if cs==1 || cs==2
veus = base_dir + "/veus"


#####################################################################################################

#PARÀMETRES GENERALS DEL SAMPLE#

#variable on guardo un enter random que equivaldrà al sample dins la carpeta starters# USUARI
numsample = rand_i(1000)
# numsample = 7

factorbtstr = rrand(1.01,1.03) if afinat == 0
factorbtstr = 1 if afinat == 1

#btstr és l'estirament de la mostra. El calculo amb la duració del sample * un factor que depèn del tempo per evitar que quan el tempo
#és lent l'estiramennt sigui molt gran i sona massa greu i amb el típic so defectuós d'stretching
btstr = ((sample_duration starters, numsample)*(current_bpm/current_bpm*factorbtstr))

########################################################################################################

#PARÀMETRES DE LES VEUS#
sampveu = rand_i(10000)
# sampveu = 9

######################################################################################################

#PARÀMETRES DEL TRACTAMENT AGUT DEL SAMPLE#

########relació entre agut i greu
rel = 1 
#el volum del sample agut depèn de la variable cs (complexitat del sàmpler): si val 1 o 3 no sona el sample agut.
vsa = 0 if cs==1 || cs==3
vsa = 0.45 if (cs==2 || cs==4) && afinat==0
vsa = 0.25 if (cs==2 || cs==4) && afinat==1
puts vsa
#vsa = 0
#retard del sample agut. Per donar groove.
delaysampagut = rrand(0.02,0.08) + modifdelaysampagut
#cutoff del sample, com més alt més brillant el sample
sco = rrand(76,84) if afinat==0
sco = rrand(85,95) if afinat==1
puts sco
#filtre passa-aguts
hpsampagut = 79
#altres efectes evidents
echomix = rrand(0.02,0.05)
echodecay = rrand(0,1)
reverbmixagut = rrand(0.1,0.55)
panagut = choose([-0.5,0.5])
#distància entre cada shot del sample
separapad = choose([1,2])
#talls (chops) que fem al sample original
numtallsagut = (sample_duration starters, numsample)/(2)
#finalització del sample per a cada shot
fin = separapad*rrand(0.98,0.99)
#tall en el que inicio la seqüència del sample agut
inicisampagut = rrand_i(2,numtallsagut)+ desplasamp*4
#salts entre tall i tall que faig entre cada shot
saltsampagut = choose([2,3])

#####################################################################################################

#PARÀMETRES DEL TRACTAMENT GREU DEL SAMPLE#


#Volum sample greu
volsampgreu = 1.5
#volsampgreu = 0
#retard sample greu, més gran que l'agut, per donar groove
delaysampgreu = rrand(0.06,0.12) + modifdelaysampgreu 
#filtre passa greus pel sample greu. Si sona sol -sense el sample agut- ocupa més freqüències (fins a 100). Si no, tall a 85 per deixar espai a l'agut
lpsampgreu = 89 if cs==1 || cs==3
lpsampgreu  = 84 if cs==2 || cs==4
hpsampgreu = 20
#efectes obvis sample greu
reverbmixgreu = rrand(0.05,0.15)
pangreu = 0
#aquest factoramplitud és un valor que val 1 o 2 a l'atzar. A les següents variables veiem què passa depenent de cada un dels valors
factoramplitud = choose([1, 2])
#factoramplitud = 4
#u=2 if factoramplitud==4
#tant la distància entre cada shot del sample com la finalització valen 1 o 2 depent de factoramplitud
separapadsampgreu = factoramplitud
fingreu = rrand(0.98,0.99)*factoramplitud
#talls (chops) que fem al sample original
numtallsgreu = ((sample_duration starters, numsample))
#tall en el que inicio la seqüència del sample greu. És diferent si cs val 1 o 2 (és a dir, si pilla sample del carpeta starters)
#inicisampgreuprov = choose([numtallsgreu/4,2*numtallsgreu/4,3*numtallsgreu/4,(numtallsgreu/4)+1,(2*numtallsgreu/4)+1,(3*numtallsgreu/4)+1])
inicisampgreuprov = (numtallsgreu/rrand_i(1,64)).to_i
inicisampgreu = inicisampgreuprov + desplasamp*4
#salts entre tall i tall que faig entre cada shot
saltsampgreu = rrand_i(2,3) + salts*2
saltsampgreuB = rrand_i(2,3) + saltsB*2
desplasampBi = numtallsgreu/4 + desplasampB*4

#####################################################################################################

#PARÀMETRES DE LA BATERIA#

#SONS BATERIA#
bombo = rand_i(47) + canvisonsbatera
caixa = rand_i(103) + canvisonsbatera
xarles = rand_i(31) + canvisonsbatera
#DELAYS BATERIA#
#Delays poer la totalitat de la bateria alhora i per a cada so per separat. Estan randomitzats però a més
#depenen de la variable cb (complexitat del beat). Quan cb és zero el segon summand és zero.
delaybeat = (rand(0.05))+(choose([-1,1])*(cb/90))+controldelaybeat
#delaybeat = 0.3
delaykick = rand(0.087)+(choose([1,-1])*rand(cb/30))
delaysnare = rand(0.076)+(choose([1.5,-1.5])*rand(cb/30))
delayhihat = rrand(-0.01,0.05+0.005*cb)
#VOLUMS BATERIA#
volgeneral = 0.6
volkick = volgeneral*(rrand(1.8,2))
volsnare = volgeneral*(rrand(1.1,1.3))
volcaixa2 = volgeneral*(rrand(0,0.3))
volhihat = volgeneral*(rrand(0.15,0.2))

#####################################################################################################
#####################################################################################################
#####################################################################################################
########################################## LOOPS EN DIRECTE #########################################

#Claqueta per sincronitzar tots els live_loops
live_loop :click do
  sleep 1
end


#REVERB DEL TEMA
with_fx :reverb, mix: rrand(0.03,0.09), pre_mix: 1, room: rrand(0.4,0.8), damp: rrand(0.4,0.6) do

#COMPRESSOR DEL TEMA
with_fx :compressor, pre_amp: 1.5, mix: 0.7, threshold: 0.2, clamp_time: 0.01, relax_time: 0.01, amp: 0.9  do

#EQUALITZACIÓ DEL TEMA
with_fx :eq, high: 0.4, high_note: 106, high_q: 0.5 do
with_fx :eq, high: 0.4, high_note: 98, high_q: 1 do
with_fx :eq, mid: 0.3, mid_note: 34, mid_q: 0.5 do

################################################### VEUS #################################################

#COMPRESSOR DE LES VEUS
with_fx :compressor, pre_amp: 1.2 do

#LIVE_LOOP DE LES VEUS
live_loop :veus, sync: :click do
    sleep +1+(delaybeat)*rrand(1,1.02)
    sample veus, sampveu, amp: 0.8 , rate: current_bpm/90
    sleep (sample_duration veus, sampveu)-(delaybeat)*rrand(1,1.02)
end
end

############################################### SAMPLE AGUT ################################################


#COMPRESSOR  DEL SAMPLE AGUT#
with_fx :compressor, amp: vsa, pre_amp: 1.3, amp: 1 do

#EQUALITZACIÓ DEL SAMPLE AGUT#
with_fx :eq, high: 0.3, high_note: 106, high_q: 2 do
with_fx :eq, high: 0.2, high_note: 85, high_q: 2 do
with_fx :eq, mid: -0.3, mid_note: 70, mid_q: 4 do

with_fx :hpf, cutoff: 53 do
  with_fx :eq, high: 0.1, high_note: 102, high_q: 2,
    low: -0.3, low_note: 59, low_q: 3.5, mid: 0.2, mid_note: 82,
  mid_q: 5, high_shelf: 0.3, high_shelf_note: 90, high_shelf_slope: 0.5 do

#ALTRES EFECTES SAMPLE AGUT#
with_fx :echo, mix: echomix, decay: echodecay do
with_fx :reverb, mix: reverbmixagut do

#LIVE_LOOP SAMPLE AGUT#
      live_loop :sampAgut, sync: :click do
        4.times do
          i = inicisampagut
          4.times do
            sleep delaysampagut
            sample starters, numsample, num_slices: numtallsagut, hpf: hpsampagut, slice: i, beat_stretch: btstr, cutoff: sco, finish: fin, attack: 0.03, decay: 0.9, release: 0.03, rate: 1*rel, amp: vsa, pan: panagut
            sleep separapad-delaysampagut
            i=i+saltsampagut
          end
        end
        4.times do
          i = inicisampagut+numtallsagut/2
          4.times do
            sleep delaysampagut
            sample starters, numsample, num_slices: numtallsagut, hpf: hpsampagut, slice: i, beat_stretch: btstr, cutoff: sco, finish: fin, attack: 0.03, decay: 0.9, release: 0.03, rate: 1*rel, amp: vsa, pan: panagut
            sleep separapad-delaysampagut
            i=i+saltsampagut
          end
        end
      end

end
end
end
end
end
end

end
end

########################################## SAMPLE GREU #######################################################


#EQUALITZACIÓ DEL SAMPLE GREU#
with_fx :eq, high: -0.2, high_note: 100, high_q: 2 do
with_fx :eq, mid: 0.2, mid_note: 88, mid_q: 2 do
with_fx :eq, mid: -0.6, mid_note: 70, mid_q: 4 do
with_fx :eq, low: -0.4, low_note: 55, low_q: 5  do
with_fx :eq, low: -0.7 , low_note: 35, high_q: 3 do

with_fx :hpf, cutoff: 40 do
  with_fx :eq, high: -0.2, high_note: 97, high_q: 1.8,
    low: -0.4, low_note: 53, low_q: 5, mid: -0.3, mid_note: 72,
  mid_q: 4.2, high_shelf: -0.3, high_shelf_note: 90, high_shelf_slope: 0.5 do

#COMPRESSOR DEL SAMPLE GREU#
with_fx :compressor, pre_amp: 1.6, amp: 1.1 do

#LIVE_LOOP DEL SAMPLE GREU#
live_loop :sampGreu31o62, sync: :click do

    m.times do
      y.times do
        i = inicisampgreu
        u.times do
          sleep delaysampgreu
          with_fx :reverb, mix: reverbmixgreu, room: 0.6  do
            sample starters, numsample, norm: 0, num_slices: numtallsgreu, slice: i, beat_stretch: btstr, finish: fingreu, lpf: lpsampgreu, hpf: hpsampgreu, attack: 0.03, rate: 1, amp: volsampgreu, pan: pangreu
            sleep separapadsampgreu-delaysampgreu
          end
          i = i+saltsampgreu+1
        end
      end
      z.times do
        i = inicisampgreu+4+desplasampC
        u.times do
          sleep delaysampgreu
          with_fx :reverb, mix: reverbmixgreu, room: 0.6  do
            sample starters, numsample, norm: 0, num_slices: numtallsgreu, slice: i, beat_stretch: btstr, finish: fingreu, lpf: lpsampgreu, hpf: hpsampgreu, attack: 0.03, rate: 1, amp: volsampgreu, pan: pangreu
            sleep separapadsampgreu-delaysampgreu
          end
          i = i+saltsampgreuC+rrand_i(1,2)+1
        end
      end
    end
    w.times do
      y.times do
        i = inicisampgreu+desplasampBi
        u.times do
          sleep delaysampgreu
          with_fx :reverb, mix: reverbmixgreu, room: 0.6  do
            sample starters, numsample, norm: 0, num_slices: numtallsgreu, slice: i, beat_stretch: btstr, finish: fingreu, lpf: lpsampgreu, hpf: hpsampgreu, attack: 0.03, rate: 1, amp: volsampgreu, pan: pangreu
            sleep separapadsampgreu-delaysampgreu
          end
        i = i+saltsampgreuB+1
        end
      end  
      z.times do
        i = inicisampgreu+desplasampBi+4+desplasampBC
        u.times do
         sleep delaysampgreu
          with_fx :reverb, mix: reverbmixgreu, room: 0.6  do
            sample starters, numsample, norm: 0, num_slices: numtallsgreu, slice: i, beat_stretch: btstr, finish: fingreu, lpf: lpsampgreu, hpf: hpsampgreu, attack: 0.03, rate: 1, amp: volsampgreu, pan: pangreu
            sleep separapadsampgreu-delaysampgreu
        end
        i = i+saltsampgreuBC+rrand_i(1,2)+1
      end
    end
  end
  end
end
end
end
end
end
end
end
end
end


################################################# BATERIES ####################################################

#variable que depèn de cb i que modifica l'sleep entre bombos.
k = cb*2*(rrand(-0.015,0.015))

#COMPRESSOR DE TOTES LES BATERIES
with_fx :compressor, pre_amp: 1.4, amp: 1  do

#EQ de totes les bateries#

with_fx :hpf, cutoff: 15 do
  with_fx :eq, high: -0.2, high_note: 50, high_q: 6.5,
    low: 0.2, low_note: 40, low_q: 5, mid: -0.1, mid_note: 82,
  mid_q: 5.5, high_shelf: -0.1, high_shelf_note: 123 do

#LIVE_LOOP DEL BOMBO
live_loop :kick, sync: :click do
  with_fx :compressor, pre_amp: 1, amp: volkick do
    with_fx :lpf, cutoff: 112 do

      sleep delaybeat
      sleep delaykick

      sample bd, bombo
      sleep 0.93+k
      sample bd, bombo if one_in(3) #sona 1 de cada 3 vegades
      sleep 0.72-k
      sample bd, bombo if one_in(2) #sona 1 de cada 2 vegades
      sleep 0.74+k
      sample bd, bombo
      sleep 1.7-k
      sample bd, bombo
      sleep 0.83+k
      sample bd, bombo if one_in(4) #sona 1 de cada 4 vegades
      sleep 0.97-k
      sample bd, bombo
      sleep 0.5+k
      sample bd, bombo
      sleep 1.6-k-delaykick-delaybeat

    end
  end
end

#variable que depèn de cb i que modifica l'sleep entre caixes.
s = cb*2*(rrand(-0.013,0.013))

#variable que faig servir dins l'sleep de la caixa perquè s no sigui sempre positiva, cosa que faria que la caixa sempre es desplacés "endavant"
a = dice 2

#LIVE_LOOP DE LA CAIXA
live_loop :snare, sync: :click do

  with_fx :compressor, pre_amp: 1, amp: volsnare do
    with_fx :lpf, cutoff: 112 do
      sleep delaybeat
      sleep delaysnare
      sleep 1.02 + ((-1)**(a))*s
      sample sn, caixa if one_in(16)==false #no sona 1 de cada 16 vegades
      sleep 2 + ((-1)**(a+1))*s
      sample sn, caixa if one_in(8)==false #no sona 1 de cada 8 vegades
      sleep 0.85
      sample sn, caixa, amp: volcaixa2 if one_in(6) #només sona 1 de cada 6 vegades
      sleep 1.15 + ((-1)**(a))*s
      sample sn, caixa
      sleep 2 + ((-1)**(a+1))*s
      sample sn, caixa if one_in(4)==false #no sona 1 de cada vegades
      sleep 0.85
      sample sn, caixa, amp: volcaixa2 if one_in(4) #només sona 1 de cada 4 vegades
      sleep 0.13-delaysnare-delaybeat
    end
  end
end

#variable que depèn de cb i que modifica l'sleep entre xarles
x = cb*3*(rand(0.035))

live_loop :hihat, sync: :click do
puts cb
  with_fx :compressor, pre_amp: 1, amp: volhihat do
    with_fx :reverb, pre_mix: 0.8, mix: 0.25 do
      sleep delaybeat
      sleep delayhihat
      sample hh, xarles, hpf: 1, cutoff: 112 if one_in(15)==false #1 de cada 15 vegades no sona
      sleep 0.52-x
      sample hh, xarles
      sleep 0.48+x
      sample hh, xarles, hpf: 1, cutoff: 90
      sleep 0.52-x
      sample hh, xarles if one_in(6)==false #1 de cada 6 vegades no sona
      sleep 0.48+x-delayhihat-delaybeat
    end
  end
end
end

end
end
end
end
end
end
"""