__author__ = 'marcos'
import numpy as np
import matplotlib
import numpy
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from itertools import cycle
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram
from fastcluster import *


class Plotter:
    def __init__(self):
        pass

    @staticmethod
    def plot_subplot_curve(pd_datas, title=None, x_label=None, y_label=None, output_filename=None, titles=None,
                           legends=None, figsize=(3, 2), marker=".", linestyle='-', markersize=10,
                           linewidth=1, markevery=None, colors=None, ylim=None, xlim=None,
                           xticks_args=None, yticks_args=None, font_size=9, font_family='normal', font_weight='normal',
                           grid=False, tight_layout=None, x_scale='linear', y_scale='linear', **kwargs):
        if pd_datas is not None:
            font = {'family': font_family,
                    'weight': font_weight,
                    'size': font_size}
            matplotlib.rc('font', **font)
            f, axs = plt.subplots(1, len(pd_datas), sharey=True, figsize=figsize)
            ls = linestyle
            #ax3 = fig.add_subplot(plot_gridspec[4, 2])
            if marker:
                if type(marker) is not list:
                    marker = [marker]
            else:
                marker = [None]
            markercycler = cycle(marker)

            lines = ["-", "--", "-.", ":"]  # matplotlib.markers.MarkerStyle.markers.keys() #
            linecycler = cycle(lines)
            xlim_min = float('inf')
            xlim_max = float('-inf')
            colorcycler = None
            legendcycler = None
            if legends:
                legendcycler = cycle(legends)
            if colors:
                colorcycler = cycle(colors)
            if y_label:
                axs[0].set_ylabel(y_label)
            # if y_label:
            #     f.text(0.08, 0.5, y_label, ha='center', va='center', rotation='vertical')
            if x_label:
                f.text(0.5, 0.01, x_label, ha='center', va='center')
            for data_i in range(len(pd_datas)):
                markevery_ = markevery
                pd_data = pd_datas[data_i]
                ax = axs[data_i]
                if grid:
                    ax.grid()
                for pd_data_i in pd_data:
                    legend_title = None
                    if legends:
                        legend_title = cycle(legendcycler)
                    if not linestyle:
                        ls = next(linecycler)
                    if colorcycler:
                        ax.plot(pd_data_i['x'], pd_data_i['y'], linestyle=ls,
                                marker=next(markercycler), label=next(legend_title),
                                markersize=markersize, linewidth=linewidth,
                                markevery=markevery_, color=next(colorcycler), **kwargs)
                    else:
                        ax.plot(pd_data_i['x'], pd_data_i['y'], linestyle=ls,
                                marker=next(markercycler), label=next(legend_title),
                                markersize=markersize, linewidth=linewidth,
                                markevery=markevery_, **kwargs)
                    if markevery_:
                        markevery_ += 1
                    #plt.legend(loc=2)
                    xlim_min = min(xlim_min, min(pd_data_i['x']))
                    xlim_max = max(xlim_max, max(pd_data_i['x']))
                    if titles:
                        ax.set_title(titles[data_i])
                    if ylim:
                        ax.set_ylim(ylim)
                    # if y_label:
                    #     ax.set_ylabel(y_label)
                    if x_scale:
                        ax.set_xscale(x_scale)
                    if y_scale:
                        ax.set_yscale(y_scale)
                    if xticks_args:
                        ax.xticks(*xticks_args)
                    if yticks_args:
                        ax.yticks(*yticks_args)
                    if xlim:
                        ax.set_xlim(xlim)
                    else:
                        ax.set_xlim(xlim_min, xlim_max)
            plt.legend(loc=4)
            if tight_layout is not None:
                if not tight_layout:
                    plt.tight_layout()
                else:
                    plt.tight_layout(rect=tight_layout)
            if title:
                plt.suptitle(title)
            if output_filename:
                plt.savefig(output_filename)
                #plt.clf()
                plt.close()
            else:
                plt.show()

    @staticmethod
    def plot_curve(pd_data, title=None, x_label=None, y_label=None, output_filename=None,
                   legends=None, figsize=(3, 2), marker=".", linestyle='-', markersize=10, loc=2, loc_anchor=False,
                   linewidth=1, markevery=None, colors=None, ylim=None, xlim=None, vline_at=None,
                   xticks_args=None, font_size=9, font_family='normal', font_weight='normal',
                   yticks_args=None, grid=False, tight_layout=None, x_scale='linear', annotate=None,
                   y_scale='linear', legend_ncol=1,  xtick_rotation=0, **kwargs):
        if pd_data is not None:
            font = {'family': font_family,
                    'weight': font_weight,
                    'size': font_size}
            matplotlib.rc('font', **font)
            fig = plt.figure(figsize=figsize)
            ls = linestyle
            #ax3 = fig.add_subplot(plot_gridspec[4, 2])
            if marker:
                if type(marker) is not list:
                    marker = [marker]
            else:
                marker = [None]
            markercycler = cycle(marker)
            if type(pd_data) is not list:
                plt.plot(pd_data['x'], pd_data['y'], linestyle=linestyle, linewidth=linewidth, markersize=markersize,
                         marker=next(markercycler), markevery=markevery, color=colors, **kwargs)
                if xlim:
                    plt.xlim(xlim)
                else:
                    plt.xlim(min(pd_data['x']), max(pd_data['x']))
            else:
                lines = ["-", "--", "-.", ":"]  # matplotlib.markers.MarkerStyle.markers.keys() #
                linecycler = cycle(lines)
                xlim_min = float('inf')
                xlim_max = float('-inf')
                colorcycler = None
                legendcycler = None
                if legends:
                    legendcycler = cycle(legends)
                if colors:
                    colorcycler = cycle(colors)
                for pd_data_i in pd_data:
                    legend_title = None
                    if legends:
                        legend_title = cycle(legendcycler)
                    if not linestyle:
                        ls = next(linecycler)
                    if colorcycler:
                        plt.plot(pd_data_i['x'], pd_data_i['y'], linestyle=ls,
                                 marker=next(markercycler), label=next(legend_title),
                                 markersize=markersize, linewidth=linewidth,
                                 markevery=markevery, color=next(colorcycler), **kwargs)
                    else:
                        plt.plot(pd_data_i['x'], pd_data_i['y'], linestyle=ls,
                                 marker=next(markercycler), label=next(legend_title),
                                 markersize=markersize, linewidth=linewidth,
                                 markevery=markevery, **kwargs)
                    if markevery:
                        markevery += 1
                    if not loc_anchor:
                        plt.legend(loc=loc, numpoints=1, framealpha=1.0, handletextpad=0.1, borderpad=0.2,
                                   ncol=legend_ncol)
                    else:
                        plt.legend(bbox_to_anchor=(1.01, 1), loc=loc, borderaxespad=0., numpoints=1, ncol=legend_ncol)
                    leg = plt.gca().get_legend()
                    ltext = leg.get_texts()  # all the text.Text instance in the legend
                    plt.setp(ltext, fontsize='medium')    # the legend text fontsize
                    xlim_min = min(xlim_min, min(pd_data_i['x']))
                    xlim_max = max(xlim_max, max(pd_data_i['x']))
                if xlim:
                    plt.xlim(xlim)
                else:
                    plt.xlim(xlim_min, xlim_max)
            if vline_at is not None:
                plt.axvline(x=vline_at)
            if annotate:
                fig.text(*annotate)
            if x_scale:
                plt.xscale(x_scale)
            if y_scale:
                plt.yscale(y_scale)
            if xticks_args:
                plt.xticks(*xticks_args, rotation=xtick_rotation)
            if yticks_args:
                plt.yticks(*yticks_args)
            if grid:
                plt.grid()
            if ylim:
                plt.ylim(ylim)
            if x_label:
                plt.xlabel(x_label)
            if y_label:
                plt.ylabel(y_label)
            if title:
                plt.suptitle(title, horizontalalignment='center')
            if tight_layout is not None:
                if not tight_layout:
                    plt.tight_layout()
                else:
                    plt.tight_layout(rect=tight_layout)
            if output_filename:
                plt.savefig(output_filename)
                #plt.clf()
                plt.close()
            else:
                plt.show()

    @staticmethod
    def create_heatmap(matrix,
                       main_title=None,
                       output_filename=None,
                       pd_data_1=None,
                       pd_data_2=None,
                       data_hist_1=None,
                       data_hist_2=None,
                       graphs=None,
                       ordered=False,
                       fitness_slice=500):
        matrixdf = pd.DataFrame(matrix)
        font = {'family': 'normal',
                'weight': 'normal',
                'size': 8}
        last_data_1 = 0.0
        matplotlib.rc('font', **font)
        # look at raw data
        #axi = plt.imshow(matrixdf,interpolation='nearest')
        #ax = axi.get_axes()

        #plt.clean_axis(ax)

        # row clusters
        if ordered:
            row_pairwise_dists = squareform(pdist(matrixdf))
            row_clusters = linkage(row_pairwise_dists, method='complete')
            row_dendogram = dendrogram(row_clusters, no_plot=True, count_sort='ascending')

        # calculate pairwise distances for columns
        if ordered:
            col_pairwise_dists = squareform(pdist(matrixdf.T))
            col_clusters = linkage(col_pairwise_dists, method='complete')
            col_dendogram = dendrogram(col_clusters, no_plot=True, count_sort='ascending')

        # plot the results
        fig = plt.figure(figsize=(12.5, 10))
        #plot_gridspec = gridspec.GridSpec(3,2, wspace=0.05,
        #  hspace=0.05, width_ratios=[0.25,1],height_ratios=[0.25,1,0.25])
        plot_gridspec = gridspec.GridSpec(5, 5, width_ratios=[0.15, 0.15, 0.2, 0.2, 0.2])

        ### col dendrogram ####
        #col_denAX = fig.add_subplot(plot_gridspec[0,1])
        if pd_data_1 is not None:
            title = ''
            if type(pd_data_1) == tuple:  # not so pythonic
                title = pd_data_1[0]
                pd_data_1 = pd_data_1[1]
            last_data_1 = pd_data_1['y'][len(pd_data_1)-1]

            #ax3 = fig.add_subplot(plot_gridspec[0,1])
            ax1 = plt.subplot(plot_gridspec[0, 2:])
            slice_base = max(0, len(pd_data_1) - fitness_slice)
            plt.plot(pd_data_1['x'], pd_data_1['y'], linestyle='-')
            plt.xlim(slice_base, len(pd_data_1))
            plt.title(title)
    #     else:
    #         col_denAX = fig.add_subplot(plot_gridspec[0,1])
        #create an empty graph

        ### row dendrogram ###
        ## t ODO: fix that please:
        if ordered:
            pass
            #row_denAX = fig.add_subplot(plot_gridspec[1,0])
            #row_denD = dendrogram(row_clusters, orientation='right', count_sort='ascending')
            #row_denAX.get_xaxis().set_ticks([]) # removes ticks

            #slice_base = max(0, max(pd_data_1['x']) - fitness_slice)
            #plt.plot(pd_data_1['x'], pd_data_1['y'], linestyle='-')
            #plt.xlim(slice_base, len(pd_data_1))

        if graphs is not None:
            gs_index = 0
            for title_graph in graphs:
                title, graph, graph_histogram = title_graph
                ax3 = plt.subplot(plot_gridspec[gs_index, 0])
                graph = graph.to_undirected()
                # we don't care about the weight because we already are filtering here
                nx.draw(graph, node_size=2, width=0.4, with_labels=False,
                        pos=nx.spring_layout(graph, weight=None))
                plt.title(title)
                ax3 = plt.subplot(plot_gridspec[gs_index, 1])
                # let's add the histogram, but remove all 1 values
                graph_histogram_without_one = []
                for v in graph_histogram:
                    if v != 1:
                        graph_histogram_without_one.append(v)
                print str(graph_histogram_without_one)
#                 print str(graph_histogram)
                if not graph_histogram_without_one:
                    continue
                binwidth = 1
                min_bin = numpy.min(graph_histogram_without_one)
                max_bin = numpy.max(graph_histogram_without_one)
                bins = range(min_bin, max_bin+binwidth, binwidth)
                ax3.hist(graph_histogram_without_one, bins=bins, facecolor='red', alpha=0.45)
                plt.xticks(numpy.unique(graph_histogram_without_one))
                plt.tick_params(axis='both', which='major', labelsize=5)
                plt.tick_params(axis='both', which='minor', labelsize=5)
#                plt.xticks(range(numpy.min(graph_histogram_without_one),
#                           numpy.max(graph_histogram_without_one),
#                           (numpy.min(graph_histogram_without_one) +  numpy.max(graph_histogram_without_one))/5))
                #plt.xlim(1, numpy.max(graph_histogram))
                if gs_index == 0:
                    plt.title("Components size\nhistogram")
                gs_index += 1

        ### heatmap ###
        heatmap_subplot = fig.add_subplot(plot_gridspec[1:4, 2:])

        if ordered:
            pass
            axi = heatmap_subplot.imshow(matrixdf.ix[row_dendogram['leaves'], col_dendogram['leaves']],
                                         interpolation='nearest', aspect='auto', origin='lower')
        else:
            axi = heatmap_subplot.imshow(matrixdf, interpolation='nearest', aspect='auto', origin='lower')
        # removes ticks
        heatmap_subplot.get_xaxis().set_ticks([])
        heatmap_subplot.get_yaxis().set_ticks([])
        axcolor = fig.add_axes([0.91, 0.27, 0.02, 0.45])
        plt.colorbar(axi, cax=axcolor)
        #fig.tight_layout()

        if pd_data_2 is not None:
            title = ''
            if type(pd_data_2) == tuple:  # not so pythonic
                title = pd_data_2[0]
                pd_data_2 = pd_data_2[1]
            ax3 = fig.add_subplot(plot_gridspec[4, 2])
            plt.plot(pd_data_2['x'], pd_data_2['y'], linestyle='-', marker='.')
            plt.xlim(min(pd_data_2['x']), max(pd_data_2['x']))
            #plt.ylim(0, 1.1)
            plt.title(title)

        if data_hist_1 is not None:
            title = ''
            if type(data_hist_1) == tuple:  # not so pythonic
                title = data_hist_1[0]
                data_hist_1 = data_hist_1[1]
            #binwidth = 1
            ax3 = fig.add_subplot(plot_gridspec[4, 3])
            #min_bin = numpy.min(data_hist_1)
            #max_bin = numpy.max(data_hist_1)
            #bins = range(min_bin,max_bin+binwidth,binwidth)
            ax3.hist(data_hist_1,  facecolor='blue', alpha=0.45)
            #plt.xticks(numpy.unique(data_hist_1))
            plt.tick_params(axis='both', which='major', labelsize=5)
            plt.tick_params(axis='both', which='minor', labelsize=5)
            plt.title(title)

        if data_hist_2 is not None:
            title = ''
            if type(data_hist_2) == tuple:  # not so pythonic
                title = data_hist_2[0]
                data_hist_2 = data_hist_2[1]
            if data_hist_2:
                ax3 = fig.add_subplot(plot_gridspec[4, 4])
                #bins = range(min_bin,max_bin+binwidth,binwidth)
                ax3.hist(data_hist_2,  facecolor='blue', alpha=0.45)
                #plt.xticks(numpy.unique(data_hist_1))
                plt.tick_params(axis='both', which='major', labelsize=5)
                plt.tick_params(axis='both', which='minor', labelsize=5)
                plt.title(title)

        if main_title:
            if pd_data_1 is not None:
                main_title = main_title + '\n(' + str(last_data_1).strip() + ')'
            plt.suptitle(main_title)
        if output_filename:
            plt.savefig(output_filename)
            #plt.clf()
            plt.close()
        else:
            plt.show()

    @staticmethod
    def plot_heatmap(matrix=None, matrixdf=None, main_title=None, output_filename=None, titles=None, ordered=False,
                     font_size=9, font_family='normal', font_weight='normal', figsize=None, tight_layout=None,
                     titles_x=None, titles_y=None, values_on=False, values_on_text=None, vmin=-1.0, vmax=1.0,
                     grid=False, x_label=None, y_label=None, set_yticks=None, set_xticks=None, subplot_adjust=None,
                     colorbar_on=True, **kargs):
        assert (matrix is not None or matrixdf is not None), "Give me matrix or matrixdf!"
        if matrix is not None:
            matrixdf = pd.DataFrame(matrix)
        font = {'family': font_family,
                'weight': font_weight,
                'size': font_size}
        matplotlib.rc('font', **font)
        # look at raw data
        #axi = plt.imshow(matrixdf,interpolation='nearest')
        #ax = axi.get_axes()

        #plt.clean_axis(ax)

        # row clusters
        if ordered:
            row_pairwise_dists = squareform(pdist(matrixdf))
            row_clusters = linkage(row_pairwise_dists, method='complete')
            row_dendogram = dendrogram(row_clusters, no_plot=True, count_sort='ascending')

        # calculate pairwise distances for columns
        if ordered:
            col_pairwise_dists = squareform(pdist(matrixdf.T))
            col_clusters = linkage(col_pairwise_dists, method='complete')
            col_dendogram = dendrogram(col_clusters, no_plot=True, count_sort='ascending')

        # plot the results
        if figsize is not None:
            fig = plt.figure(figsize=figsize)
        else:
            fig = plt.figure()
        #plot_gridspec = gridspec.GridSpec(3,2, wspace=0.05,
        #  hspace=0.05, width_ratios=[0.25,1],height_ratios=[0.25,1,0.25])
        # plot_gridspec = gridspec.GridSpec(5, 5, width_ratios=[0.15, 0.15, 0.2, 0.2, 0.2])
        ### heatmap ###
        heatmap_subplot = fig.add_subplot(111)
        if titles and not titles_x:
            titles_x = titles
        if titles and not titles_y:
            titles_y = titles
        if ordered:
            axi = heatmap_subplot.matshow(matrixdf.ix[row_dendogram['leaves'], col_dendogram['leaves']],
                                          interpolation='nearest', aspect='auto', origin='lower', vmin=vmin, vmax=vmax,
                                          **kargs)
            if titles_x:
                heatmap_subplot.set_xticklabels([titles_x[i] for i in col_dendogram['leaves']], rotation=90)
            if titles_y:
                heatmap_subplot.set_yticklabels([titles_y[i] for i in row_dendogram['leaves']])
        else:
            axi = heatmap_subplot.matshow(matrixdf, interpolation='nearest', aspect='auto', origin='lower',
                                          vmin=vmin, vmax=vmax, **kargs)
            if titles_x:
                heatmap_subplot.set_xticklabels(titles_x, rotation=90)
                heatmap_subplot.tick_params(labelbottom='on', labeltop='off')
            if titles_y:
                heatmap_subplot.set_yticklabels(titles_y)
        if set_xticks:
            heatmap_subplot.set_xticks(set_xticks)
        else:
            heatmap_subplot.set_xticks(range(len(matrixdf.columns)))
        if set_yticks:
            heatmap_subplot.set_yticks(set_yticks)
        else:
            heatmap_subplot.set_yticks(range(len(matrixdf)))
        if colorbar_on:
            plt.colorbar(axi)
        values_on_text_format = '{:s}'
        if values_on_text is None:
            values_on_text = matrixdf
            values_on_text_format = '{:0.2f}'
        if values_on:
            if ordered:
                for (i, j), z in np.ndenumerate(values_on_text.ix[row_dendogram['leaves'], col_dendogram['leaves']]):
                    heatmap_subplot.text(j, i, values_on_text_format.format(z), ha='center', va='center', weight='medium')
            else:
                for (i, j), z in np.ndenumerate(values_on_text):
                    heatmap_subplot.text(j, i, values_on_text_format.format(z), ha='center', va='center', weight='medium')
        if tight_layout is not None:
            if not tight_layout:
                plt.tight_layout()
            else:
                plt.tight_layout(rect=tight_layout)
        #fig.tight_layout()
        #
        # if pd_data_2 is not None:
        #     title = ''
        #     if type(pd_data_2) == tuple:  # not so pythonic
        #         title = pd_data_2[0]
        #         pd_data_2 = pd_data_2[1]
        #     ax3 = fig.add_subplot(plot_gridspec[4, 2])
        #     plt.plot(pd_data_2['x'], pd_data_2['y'], linestyle='-', marker='.')
        #     plt.xlim(min(pd_data_2['x']), max(pd_data_2['x']))
        #     #plt.ylim(0, 1.1)
        #     plt.title(title)
        #
        # if data_hist_1 is not None:
        #     title = ''
        #     if type(data_hist_1) == tuple:  # not so pythonic
        #         title = data_hist_1[0]
        #         data_hist_1 = data_hist_1[1]
        #     #binwidth = 1
        #     ax3 = fig.add_subplot(plot_gridspec[4, 3])
        #     #min_bin = numpy.min(data_hist_1)
        #     #max_bin = numpy.max(data_hist_1)
        #     #bins = range(min_bin,max_bin+binwidth,binwidth)
        #     ax3.hist(data_hist_1,  facecolor='blue', alpha=0.45)
        #     #plt.xticks(numpy.unique(data_hist_1))
        #     plt.tick_params(axis='both', which='major', labelsize=5)
        #     plt.tick_params(axis='both', which='minor', labelsize=5)
        #     plt.title(title)
        #
        # if data_hist_2 is not None:
        #     title = ''
        #     if type(data_hist_2) == tuple:  # not so pythonic
        #         title = data_hist_2[0]
        #         data_hist_2 = data_hist_2[1]
        #     if data_hist_2:
        #         ax3 = fig.add_subplot(plot_gridspec[4, 4])
        #         #bins = range(min_bin,max_bin+binwidth,binwidth)
        #         ax3.hist(data_hist_2,  facecolor='blue', alpha=0.45)
        #         #plt.xticks(numpy.unique(data_hist_1))
        #         plt.tick_params(axis='both', which='major', labelsize=5)
        #         plt.tick_params(axis='both', which='minor', labelsize=5)
        #         plt.title(title)
        #
        if subplot_adjust:
            plt.subplots_adjust(*subplot_adjust)
        if grid:
            plt.grid()
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)
        if main_title:
            plt.suptitle(main_title)
        if output_filename:
            plt.savefig(output_filename)
            #plt.clf()
            plt.close()
        else:
            plt.show()

    @staticmethod
    def plot_boxplots(data, titles, main_title=None, ylabel=None, xlabel=None, xscale=None,
                      yscale=None, first=0, output=None, size=None, ylim=None, xlim=None, xticks_args=None,
                      font_size=9, font_family='normal', font_weight='normal', **kargs):
        # ## plot here:
        # multiple box plots on one figure
        font = {'family': font_family,
                'weight': font_weight,
                'size': font_size}
        matplotlib.rc('font', **font)
        if size:
            plt.figure(figsize=size)
        else:
            plt.figure()
        # fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
        # bp = axes[0, 0].boxplot(all_alphas, notch=0, sym='+', showmeans=True, widths=0.3)
        ax = plt.axes()
        bp = plt.boxplot(data[first:], notch=0, sym='+', showmeans=True, widths=0.3, whis=1., **kargs)
        plt.setp(bp['boxes'], color='black')
        plt.setp(bp['whiskers'], color='blue', linestyle="-")
        plt.setp(bp['fliers'], color='gray', marker='+')
        plt.setp(bp['means'], color='black', marker='.', fillstyle='none', markerfacecolor='gray', pickradius=0.2)
        # for ax in axes.flatten():
        #     ax.set_yscale('log')
        #     ax.set_yticklabels([])
        if yscale:
            ax.set_yscale(yscale)
        if xscale:
            ax.set_xscale(xscale)
        if titles:
            plt.xticks(range(1, len(data[first:]) + 1), titles[first:], rotation=90)
        if xticks_args:
            plt.xticks(xticks_args)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)
        if main_title:
            plt.title(main_title)
        plt.grid()
        plt.tight_layout()
        if not output:
            plt.show()
        else:
            plt.savefig(output)
            plt.close()

    @staticmethod
    def plot_hist(data, main_title, ylabel=None, xlabel=None, xscale=None, yscale=None, first=0,
                  size=None, output=None, xticks_args=None, ylim=None, xlim=None, **kwargs):
        if size:
            fig = plt.figure(figsize=size)
        else:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        weights = np.ones_like(data)/float(len(data))
        n, bins, patches = plt.hist(data, 50, weights=weights)
        plt.grid(True)
        if yscale:
            ax.set_yscale(yscale)
        if xscale:
            ax.set_xscale(xscale)  # if not event_type:
        plt.xlabel("Number of events")
        ax.set_title(main_title)
        plt.title(main_title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        if ylim:
            plt.ylim(ylim)
        if xlim:
            plt.xlim(xlim)
        # plt.ylim((0.005, 0.2))
        plt.grid()
        plt.tight_layout()
        if xticks_args:
            plt.xticks(*xticks_args)
        #plt.show()
        # plt.savefig(png_file)
        # plt.close()
        # plt.xlabel("$n$ (number of crimes)")
        # plt.ylabel("$P(N>n)$")
        # plt.grid()
        # plt.tight_layout()
        # fig.legend(loc=1, numpoints=1)
        if not output:
            plt.show()
        else:
            plt.savefig(output)
            plt.close()

    @staticmethod
    def plot_cuvve(pd_data, title=None, x_label=None, y_label=None, output_filename=None,
                   legends=None, figsize=(3, 2), marker=".", linestyle='-', markersize=10, loc=2, loc_anchor=False,
                   linewidth=1, markevery=None, colors=None, ylim=None, xlim=None, vline_at=None,
                   xticks_args=None, font_size=9, font_family='normal', font_weight='normal',
                   yticks_args=None, grid=False, tight_layout=None, x_scale='linear', annotate=None,
                   y_scale='linear', legend_ncol=1,  xtick_rotation=0, **kwargs):
        if pd_data is not None:
            font = {'family': font_family,
                    'weight': font_weight,
                    'size': font_size}
            matplotlib.rc('font', **font)
            fig = plt.figure(figsize=figsize)
            ls = linestyle
            #ax3 = fig.add_subplot(plot_gridspec[4, 2])
            if marker:
                if type(marker) is not list:
                    marker = [marker]
            else:
                marker = [None]
            markercycler = cycle(marker)
            if type(pd_data) is not list:
                plt.plot(pd_data['x'], pd_data['y'], linestyle=linestyle, linewidth=linewidth, markersize=markersize,
                         marker=next(markercycler), markevery=markevery, color=colors, **kwargs)
                if xlim:
                    plt.xlim(xlim)
                else:
                    plt.xlim(min(pd_data['x']), max(pd_data['x']))
            else:
                lines = ["-", "--", "-.", ":"]  # matplotlib.markers.MarkerStyle.markers.keys() #
                linecycler = cycle(lines)
                xlim_min = float('inf')
                xlim_max = float('-inf')
                colorcycler = None
                legendcycler = None
                if not legends:
                    legends = [None]
                if legends:
                    legendcycler = cycle(legends)
                if colors:
                    colorcycler = cycle(colors)
                for pd_data_i in pd_data:
                    legend_title = None
                    if legends:
                        legend_title = cycle(legendcycler)
                    if not linestyle:
                        ls = next(linecycler)
                    if colorcycler:
                        plt.plot(pd_data_i['x'], pd_data_i['y'], linestyle=ls,
                                 marker=next(markercycler), label=next(legend_title),
                                 markersize=markersize, linewidth=linewidth,
                                 markevery=markevery, color=next(colorcycler), **kwargs)
                    else:
                        plt.plot(pd_data_i['x'], pd_data_i['y'], linestyle=ls,
                                 marker=next(markercycler), label=next(legend_title),
                                 markersize=markersize, linewidth=linewidth,
                                 markevery=markevery, **kwargs)
                    if markevery:
                        markevery += 1
                    if not loc_anchor:
                        plt.legend(loc=loc, numpoints=1, framealpha=1.0, handletextpad=0.1, borderpad=0.2,
                                   ncol=legend_ncol)
                    else:
                        plt.legend(bbox_to_anchor=(1.01, 1), loc=loc, borderaxespad=0., numpoints=1, ncol=legend_ncol)
                    if legends[0] is not None:
                        leg = plt.gca().get_legend()
                        ltext = leg.get_texts()  # all the text.Text instance in the legend
                        plt.setp(ltext, fontsize='medium')    # the legend text fontsize
                    xlim_min = min(xlim_min, min(pd_data_i['x']))
                    xlim_max = max(xlim_max, max(pd_data_i['x']))
                if xlim:
                    plt.xlim(xlim)
                else:
                    plt.xlim(xlim_min, xlim_max)
            if vline_at is not None:
                plt.axvline(x=vline_at)
            if annotate:
                fig.text(*annotate)
            if x_scale:
                plt.xscale(x_scale)
            if y_scale:
                plt.yscale(y_scale)
            if xticks_args:
                plt.xticks(*xticks_args, rotation=xtick_rotation)
            if yticks_args:
                plt.yticks(*yticks_args)
            if grid:
                plt.grid()
            if ylim:
                plt.ylim(ylim)
            if x_label:
                plt.xlabel(x_label)
            if y_label:
                plt.ylabel(y_label)
            if title:
                plt.suptitle(title, horizontalalignment='center')
            if tight_layout is not None:
                if not tight_layout:
                    plt.tight_layout()
                else:
                    plt.tight_layout(rect=tight_layout)
            if output_filename:
                plt.savefig(output_filename)
                #plt.clf()
                plt.close()
            else:
                plt.show()

    @staticmethod
    def plot_curve(x, y, main_title, ylabel=None, xlabel=None, xscale=None, yscale=None, first=0,
                   size=None, output=None, xticks_args=None, ylim=None, xlim=None, vline_at=None, hline_at=None,
                   **kwargs):
        Plotter.plot_curves([(x, y)], main_title, ylabel=ylabel, xlabel=xlabel, xscale=xscale, yscale=yscale,
                            first=first, size=size, output=output, xticks_args=xticks_args, ylim=ylim, xlim=xlim,
                            vline_at=vline_at, hline_at=hline_at, **kwargs)

    @staticmethod
    def plot_curves(curves, main_title, ylabel=None, xlabel=None, xscale=None, yscale=None, first=0,
                    size=None, output=None, xticks_args=None, ylim=None, xlim=None, vline_at=None, hline_at=None,
                    **kwargs):
        if size:
            fig = plt.figure(figsize=size)
        else:
            fig = plt.figure()
        ax = fig.add_subplot(111)
        if vline_at is not None:
            ax.axvline(x=vline_at)
        if hline_at is not None:
            ax.axhline(y=hline_at)
        for x, y in curves:
            if not x:
                x = range(len(y))
            ax.plot(x[first:], y[first:], **kwargs)
        if yscale:
            ax.set_yscale(yscale)
        if xscale:
            ax.set_xscale(xscale)  # if not event_type:
        # ax.set_title("Kolmogorov-Smirnov test ("+city+")")
        #     ax.set_title("Kolmogorov-Smirnov test ("+city+" - "+event_type+")")
        # else:
        plt.xlabel("Number of regions")
        plt.ylabel(ylabel)
        ax.set_title(main_title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        # plt.ylim((0.005, 0.2))
        plt.grid()
        plt.tight_layout()
        if ylim:
            plt.ylim(ylim)
        if xlim:
            plt.xlim(xlim)
        # plt.ylim((0.02, 0.04))
        if xticks_args:
            plt.xticks(*xticks_args)
        #plt.show()
        # plt.savefig(png_file)
        # plt.close()
        # plt.xlabel("$n$ (number of crimes)")
        # plt.ylabel("$P(N>n)$")
        # plt.grid()
        # plt.tight_layout()
        # fig.legend(loc=1, numpoints=1)
        if not output:
            plt.show()
        else:
            plt.savefig(output)
            plt.close()

    @staticmethod
    def plot_boxplots(data, titles, main_title, ylabel=None, xlabel=None, xscale=None,
                      yscale=None, first=0, output=None, size=None):
        # ## plot here:
        # multiple box plots on one figure
        if size:
            plt.figure(figsize=size)
        else:
            plt.figure()
        # fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
        # bp = axes[0, 0].boxplot(all_alphas, notch=0, sym='+', showmeans=True, widths=0.3)
        ax = plt.axes()
        bp = plt.boxplot(data[first:], notch=0, sym='+', showmeans=True, widths=0.3, whis=1.)
        plt.setp(bp['boxes'], color='black')
        plt.setp(bp['whiskers'], color='blue', linestyle="-")
        plt.setp(bp['fliers'], color='gray', marker='+')
        plt.setp(bp['means'], color='black', marker='.', fillstyle='none', markerfacecolor='gray', pickradius=0.2)
        # for ax in axes.flatten():
        #     ax.set_yscale('log')
        #     ax.set_yticklabels([])
        if yscale:
            ax.set_yscale(yscale)
        if xscale:
            ax.set_xscale(xscale)
        if titles:
            plt.xticks(range(1, len(data[first:]) + 1), titles[first:], rotation=90)
        # plt.ylim((0, 150))
        # plt.ylim((0.02, 0.04))
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        # plt.ylim((0, 3))
        plt.title(main_title)
        plt.grid()
        plt.tight_layout()
        if not output:
            plt.show()
        else:
            plt.savefig(output)
            plt.close()

    @staticmethod
    def plot_distributions_fit_curves(fits, legend_loc=1, titles=None, output=None, main_title=None,
                                      size=None, plot='pdf', distributions=None):
        """
            Plots the curve for each fit in fits.
        :param fits: the list of fits
        :return:
        """
        if fits:
            if size:
                fig = plt.figure(figsize=size)
            else:
                fig = plt.figure()
            if distributions is None:
                distributions = []
            for index in range(len(fits)):
                fit = fits[index]
                if plot == 'cdf':
                    fig = fit.plot_cdf(linewidth=0, marker='.', markersize=10)
                elif plot == 'ccdf':
                    fig = fit.plot_ccdf(linewidth=0, marker='.', markersize=10)
                elif plot == 'pdf':
                    fig = fit.plot_pdf(linewidth=0, marker='.', markersize=10)

                # powerlaw
                if 'power_law' in distributions:
                    x_min, alpha, d = fit.power_law.xmin, fit.power_law.alpha, fit.power_law.D
                    label_power_law = "$\\alpha$=" + "%2.2f" % alpha
                    if plot == 'cdf':
                        fit.power_law.plot_cdf(linestyle='--', label=label_power_law, ax=fig)
                    elif plot == 'ccdf':
                        fit.power_law.plot_ccdf(linestyle='--', label=label_power_law, ax=fig)
                    elif plot == 'pdf':
                        fit.power_law.plot_pdf(linestyle='--', label=label_power_law, ax=fig)

                # lognormal
                if 'lognormal' in distributions:
                    label_lognormal = "$\\mu$=" + "%2.2f" % fit.lognormal.mu + \
                                      " $\\sigma$=" + "%2.2f" % fit.lognormal.sigma
                    if plot == 'cdf':
                        fit.lognormal.plot_cdf(linestyle=':', label=label_lognormal, ax=fig)
                    elif plot == 'ccdf':
                        fit.lognormal.plot_ccdf(linestyle=':', label=label_lognormal, ax=fig)
                    elif plot == 'pdf':
                        fit.lognormal.plot_pdf(linestyle=':', label=label_lognormal, ax=fig)

                # truncated powerlaw
                if 'truncated_power_law' in distributions:
                    label_truncated = "$\\alpha$=" + "%2.2f" % fit.truncated_power_law.alpha + \
                                      " $\lambda$=" + "%2.2f" % fit.truncated_power_law.Lambda
                    if plot == 'cdf':
                        fit.truncated_power_law.plot_cdf(linestyle='--', label=label_truncated, ax=fig)
                    elif plot == 'ccdf':
                        fit.truncated_power_law.plot_ccdf(linestyle='--', label=label_truncated, ax=fig)
                    elif plot == 'pdf':
                        fit.truncated_power_law.plot_pdf(linestyle='--', label=label_truncated, ax=fig)

                # exponential
                if 'exponential' in distributions:
                    label_exponential = "$\lambda$=" + "%2.2f" % fit.exponential.Lambda
                    if plot == 'cdf':
                        fit.truncated_power_law.plot_cdf(linestyle='-.', label=label_exponential, ax=fig)
                    elif plot == 'ccdf':
                        fit.truncated_power_law.plot_ccdf(linestyle='-.', label=label_exponential, ax=fig)
                    elif plot == 'pdf':
                        fit.truncated_power_law.plot_pdf(linestyle='-.', label=label_exponential, ax=fig)
            if fig:
                plt.xlabel("$n$ (number of crimes)")
                if plot == 'cdf':
                    plt.ylabel("$P(N\\leq n)$")  # cumulative distribution function
                elif plot == 'ccdf':
                    plt.ylabel("$P(N>n)$")  # complementary cumulative distribution function
                elif plot == 'pdf':
                    plt.ylabel("$p(n)$")  # probability density function
                plt.grid()
                plt.tight_layout()
                fig.legend(loc=legend_loc, numpoints=1)
                if main_title:
                    plt.title(main_title)
                if not output:
                    plt.show()
                else:
                    plt.savefig(output)
                    plt.close()
        """
execfile('plotter.py')
        """
