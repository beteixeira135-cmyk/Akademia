# Roda os controles da matriz no r3PG ORIGINAL (pacote compilado do GitHub, v0.1.7)
suppressMessages(library(r3PG))
args <- commandArgs(TRUE); B <- args[1]
par <- read.csv(file.path(B,"r_check/parametros_r3pg.csv"), check.names=FALSE)
ctl <- read.csv(file.path(B,"r_check/controles.csv"))
ini <- list(A1=c(2.07,5.47,1.09), C1=c(0.110,0.064,0.080), C2=c(0.170,0.116,0.100), C3=c(0.162,0.075,0.093),
            C4=c(0.170,0.116,0.100), C5=c(0.168,0.106,0.099))   # WF0, WS0, WR0 (fontes)
lat <- c(IND=-19.0389, TB=-24.3239, IMP=-5.52583)
res <- list()
for (i in seq_len(nrow(ctl))) {
  r <- ctl[i,]; clim <- read.csv(file.path(B, sprintf("../clima/power_api/clima_r3pg_mensal_%s.csv", r$sitio)))
  site <- data.frame(latitude=lat[[r$sitio]], altitude=0, soil_class=-1, asw_i=r$asw_max, asw_min=0, asw_max=r$asw_max,
                     from=r$inicio, to=r$fim)
  v <- ini[[r$material]]
  sp <- data.frame(species=r$material, planted=r$plantio, fertility=r$FR, stems_n=10000/9,
                   biom_stem=v[2], biom_root=v[3], biom_foliage=v[1])
  o <- run_3PG(site, sp, clim[,c("year","month","tmp_min","tmp_max","tmp_ave","prcp","srad","frost_days","vpd_day")],
               NULL, par[,c("parameter", r$material)], NULL,
               settings=list(light_model=1,transp_model=1,phys_model=1,height_model=1,correct_bias=0,calculate_d13c=0),
               check_input=TRUE, df_out=TRUE)
  o <- o[o$variable %in% c("biom_stem","biom_foliage","biom_root","volume","lai","stems_n","dbh","height"), c("date","variable","value")]
  o$id <- r$id; res[[i]] <- o
}
write.csv(do.call(rbind,res), file.path(B,"r_check/r3pg_controles.csv"), row.names=FALSE)
cat("controles rodados no r3PG:", nrow(ctl), "\n")
